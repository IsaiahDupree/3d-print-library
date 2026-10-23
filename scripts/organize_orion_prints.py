#!/usr/bin/env python3
"""Run on Orion: preserve sources, index print assets, verify a V400 backup."""
import argparse
import collections
import datetime
import hashlib
import html
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

EXTENSIONS = {'.stl', '.step', '.stp', '.3mf', '.obj', '.fcstd', '.gcode', '.scad', '.blend', '.f3d', '.iges', '.igs', '.ply', '.amf', '.sldprt', '.sldasm', '.ipt', '.iam', '.dxf', '.dwg', '.skp', '.zip', '.7z'}
SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', '.ac_files.backup'}

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''):
            h.update(b)
    return h.hexdigest()

def get(base, route):
    with urllib.request.urlopen(base + route, timeout=120) as response:
        return json.load(response)['result']

def run(args):
    root = Path(args.library)
    root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    receipt = root / 'Receipts' / (stamp + '.jsonl')
    receipt.parent.mkdir(exist_ok=True)
    def record(event, **fields):
        with receipt.open('a', encoding='utf-8') as f:
            f.write(json.dumps(dict(event=event, **fields))+'\n')
    record('started', roots=args.source_root)
    expected = {x['path']: x for x in json.loads(Path(args.baseline).read_text())['files']}
    live = get(args.printer_url, '/server/files/list?root=gcodes')
    live_paths = {x['path'] for x in live}
    if live_paths != set(expected):
        raise RuntimeError('Printer paths changed from reviewed baseline; refresh baseline before backup')
    backup = root / '01_V400_Printer_Backup'
    rows = []
    for i, item in enumerate(live, 1):
        rel = Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('Unsafe printer path')
        dest = backup / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        sha = expected[item['path']]['sha256']
        if args.index_only and not dest.exists():
            rows.append(dict(path=item['path'], sha256=sha, size=expected[item['path']]['size'], verified=False))
            continue
        if not dest.exists() or digest(dest) != sha:
            if args.index_only:
                raise RuntimeError('Existing backup hash mismatch: '+item['path'])
            temp = dest.with_name(dest.name + '.partial')
            with urllib.request.urlopen(args.printer_url+'/server/files/gcodes/'+urllib.parse.quote(item['path']), timeout=120) as response, temp.open('wb') as output:
                while True:
                    block = response.read(1024*1024)
                    if not block: break
                    output.write(block)
            if digest(temp) != sha:
                raise RuntimeError('Backup hash mismatch: '+item['path'])
            os.replace(temp, dest)
            record('backup_verified', path=item['path'], sha256=sha, size=dest.stat().st_size)
        rows.append(dict(path=item['path'], sha256=sha, size=dest.stat().st_size, verified=True))
        if i % 25 == 0: print('Verified backup', i, '/', len(live), flush=True)
    assets=[]
    for source_root in args.source_root:
        origin=Path(source_root)
        if not origin.is_dir(): raise RuntimeError('Missing source root: '+source_root)
        for directory, dirs, files in os.walk(origin, followlinks=False):
            dirs[:]=sorted(d for d in dirs if d.casefold() not in SKIP and not (Path(directory)/d).is_symlink() and not (getattr((Path(directory)/d).lstat(), 'st_file_attributes', 0) & 1024))
            for name in sorted(files):
                p=Path(directory)/name
                if p.suffix.lower() not in EXTENSIONS: continue
                rel=p.relative_to(origin)
                depth=1
                if rel.parts[0] == 'jobs' and len(rel.parts)>2: depth=2
                if len(rel.parts)>3 and rel.parts[:2] == ('modeling','jobs'): depth=3
                project='/'.join(rel.parts[:depth]) if len(rel.parts)>1 else 'Loose_Files_To_Review'
                category=origin.name+'/'+project
                assets.append(dict(path=str(p), category=category, size=p.stat().st_size, format=p.suffix.lower(), evidence='source_location_only', project_folder=str(origin.joinpath(*rel.parts[:depth])) if len(rel.parts)>1 else str(origin)))
    groups=collections.defaultdict(list)
    for item in assets: groups[item['category']].append(item)
    out=['<!doctype html><meta charset="utf-8"><title>Orion Print Library</title><style>body{font:16px system-ui;max-width:1100px;margin:40px auto;padding:20px}li{margin:7px}summary{cursor:pointer;font-weight:bold}input{padding:12px;width:90%}details{margin:20px 0}</style><h1>Orion Print Library</h1>', '<p>V400 print files and original design files. Original project paths are preserved. Folder grouping does not establish authorship, print readiness, or physical fit.</p>', '<input placeholder="Filter files by name or path" oninput="document.querySelectorAll(\'li\').forEach(x=>x.hidden=!(x.dataset.search||x.textContent).toLowerCase().includes(this.value.toLowerCase()))">', '<h2>V400: project folders and numbered files</h2>']
    out.append('<p>Backup verified: '+str(sum(x['verified'] for x in rows))+' / '+str(len(rows))+' files. Pending links open the printer copy.</p>')
    printer_groups=collections.defaultdict(list)
    for item in rows: printer_groups[item['path'].split('/')[0]].append(item)
    for group, files in sorted(printer_groups.items()):
        out.append('<details><summary>'+html.escape(group)+' ('+str(len(files))+')</summary><ul>')
        for item in sorted(files,key=lambda x:x['path']):
            url=(backup/Path(item['path'])).as_uri() if item['verified'] else args.printer_url+'/server/files/gcodes/'+urllib.parse.quote(item['path'])
            out.append('<li><a href="'+html.escape(url,quote=True)+'">'+html.escape(item['path'])+'</a>'+(' — backup verified' if item['verified'] else ' — backup pending; printer copy')+'</li>')
        out.append('</ul></details>')
    out.append('<h2>Orion original design and legacy print files</h2>')
    links=root/'02_Source_Project_Links'; links.mkdir(exist_ok=True)
    indexes=root/'03_Project_File_Indexes'; indexes.mkdir(exist_ok=True)
    out.append('<ul>')
    for group, files in sorted(groups.items()):
        key=hashlib.sha256(group.encode()).hexdigest()[:16]
        page=indexes/(key+'.html')
        out.append('<li data-search="'+html.escape(group+' '+' '.join(Path(x['path']).name for x in files),quote=True)+'"><a href="'+html.escape(page.as_uri(),quote=True)+'">'+html.escape(group)+'</a> ('+str(len(files))+' files)</li>')
        page_lines=[out[0].split('<h1>')[0], '<p><a href="../START_HERE.html">Back to library</a></p>', '<h1>'+html.escape(group)+'</h1>', '<p>Source inventory; generated revisions and archives are retained. Inclusion does not establish print readiness.</p>', out[2], '<ul>']
        for item in files:
            p=Path(item['path']); page_lines.append('<li><a href="'+html.escape(p.as_uri(),quote=True)+'">'+html.escape(str(p))+'</a></li>')
        page_lines.append('</ul>')
        page.write_text('\n'.join(page_lines),encoding='utf-8')
        target=Path(files[0]['project_folder'])
        shortcut=links/(group.replace('/',' - ').replace('\\',' - ')[:160]+ ' - '+key+'.url')
        shortcut.write_text('[InternetShortcut]\nURL='+target.as_uri()+'\n',encoding='utf-8')
    out.append('</ul>')
    (root/'START_HERE.html').write_text('\n'.join(out),encoding='utf-8')
    manifest=dict(generated_at=stamp, printer_backup=rows, source_assets=assets, source_roots=args.source_root, original_files_moved=0)
    (root/'inventory.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    summary=dict(backup_files=sum(x['verified'] for x in rows), pending_backup_files=sum(not x['verified'] for x in rows), backup_bytes=sum(x['size'] for x in rows if x['verified']), original_assets=len(assets), source_groups=len(groups), original_files_moved=0, receipt=str(receipt))
    record('completed', **summary)
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--index-only',action='store_true',help='Index sources and already completed backup files without downloading missing files')
    p.add_argument('--library',required=True)
    p.add_argument('--baseline',required=True)
    p.add_argument('--printer-url',required=True)
    p.add_argument('--source-root',action='append',required=True)
    run(p.parse_args())
