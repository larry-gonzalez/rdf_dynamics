Truthy files
============

This folder contains *truthy* rdf dumps from wikidata.

Note
----
*   There is one folder per version.
*   The date of the version is the name of the folder.
*   Original files were splited with `split` command
```
split -b 1G wikidata-20170418-truthy-BETA.nt.bz2
```
*   To join them, use
```
cat * > wikidata-20170418-truthy-BETA.nt.bz2
```
*   raw data from last ten weeks can be downloaded [here](https://dumps.wikimedia.org/wikidatawiki/entities/)
