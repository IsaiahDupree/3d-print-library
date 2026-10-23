"""Publish only receipt-linked model pictures into the local Orion library."""
import collections,hashlib,html,json,os
from pathlib import Path

def load_pictures(root):
 state=root/'04_Model_Pictures';manifest=state/'manifest.json'
 if not manifest.exists():return {},{}
 data=json.loads(manifest.read_text(encoding='utf-8'));valid={};checked={}
 for path,r in data.get('files',{}).items():
  if r.get('status')!='ready':continue
  image=Path(r['image'])
  if image.parent!=state/'images' or image.name!=r['source_sha256']+'.png':continue
  key=(str(image),r.get('image_sha256'))
  if key not in checked:checked[key]=image.is_file() and hashlib.sha256(image.read_bytes()).hexdigest()==r.get('image_sha256')
  if checked[key]:valid[path]=r
 return valid,data

def picture_html(record,width=160):
 if not record:return ''
 p=Path(record['image']);label=record['kind'].replace('_',' ')
 return '<figure style="display:inline-block;margin:8px;vertical-align:top"><a href="'+html.escape(p.as_uri(),quote=True)+'"><img loading="lazy" width="'+str(width)+'" height="'+str(width)+'" style="object-fit:contain;border-radius:12px" src="'+html.escape(p.as_uri(),quote=True)+'" alt="'+html.escape(Path(record['path']).name,quote=True)+'"></a><figcaption style="font-size:12px">'+html.escape(label)+'</figcaption></figure>'

def gallery(root,pictures,state):
 by_hash=collections.defaultdict(list)
 for r in pictures.values():by_hash[r['source_sha256']].append(r)
 out=['<!doctype html><meta charset="utf-8"><title>CAD Model Pictures</title><style>body{font:16px system-ui;background:#f4f6f9;margin:30px}#grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}.card{background:white;padding:15px;border-radius:15px;overflow-wrap:anywhere}.card[hidden]{display:none}input{padding:14px;width:90%;margin-bottom:20px}</style><p><a href="START_HERE.html">Back to library</a></p><h1>CAD Model Pictures</h1>', '<p>Click a picture to enlarge it or a filename to open the original. Matching file contents share a picture. Archive pictures show the named member; toolpath overviews are labeled.</p>', '<p>'+str(len(pictures))+' files with verified pictures; '+str(len(by_hash))+' distinct file contents. Picture job: '+html.escape(state.get('status','not started'))+'; processed '+str(state.get('processed',0))+' / '+str(state.get('total',0))+'.</p>', '<input placeholder="Search all pictured model filenames and paths" oninput="document.querySelectorAll(\'.card\').forEach(x=>x.hidden=!x.dataset.search.includes(this.value.toLowerCase()))"><div id="grid">']
 for sha,records in sorted(by_hash.items(),key=lambda x:Path(x[1][0]['path']).name.lower()):
  r=records[0];search=' '.join(x['path'] for x in records).lower()
  out.append('<article class="card" data-search="'+html.escape(search,quote=True)+'">'+picture_html(r,220)+'<p><a href="'+html.escape(Path(r['path']).as_uri(),quote=True)+'">'+html.escape(Path(r['path']).name)+'</a></p><small>'+str(len(records))+' matching file location(s)</small>')
  if r.get('member'):out.append('<p>Archive member: '+html.escape(r['member'])+'</p>')
  out.append('</article>')
 out.append('</div>')
 temp=root/'PICTURES.tmp';temp.write_text('\n'.join(out),encoding='utf-8');os.replace(temp,root/'PICTURES.html')


def file_picture(path,pictures,state):
 key=str(path)
 if key in pictures:return picture_html(pictures[key])
 r=state.get('files',{}).get(key)
 return '<small style="display:block;color:#657085">'+html.escape(('Picture unavailable: '+r.get('reason','')) if r and r.get('status')=='unavailable' else 'Picture pending')+'</small>'
