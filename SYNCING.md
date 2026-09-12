# Printables mirror process

Source profile: [@Isaiah_Dupre_1141044](https://www.printables.com/@Isaiah_Dupre_1141044)

Printables does not currently publish a supported model-upload or synchronization API. This repository therefore uses a reviewed release process rather than browser scraping or private account automation.

For each public Printables model:

1. confirm the listing is free and publicly downloadable;
2. verify Isaiah's authorship or preserve complete remix attribution;
3. confirm that the listing licence permits a GitHub mirror;
4. download the exact public files and record SHA-256 hashes;
5. create `models/<model-id>-<slug>/` with files, README, licence, source link, and approved images;
6. compare the GitHub bundle with the Printables listing;
7. update `catalog.json`, commit, and push.

Paid, club-only, private, draft, unclear-rights, and no-redistribution models are not mirrored publicly. Local CAD is never included merely because it exists on one of Isaiah's computers.

