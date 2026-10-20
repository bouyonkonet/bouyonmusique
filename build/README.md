# Build system for bouyonmusique.com

The repo root is the deployed GitHub Pages site (HTML output). This build/ folder is the source of truth for generated pages.

- generate.py builds the French pages into the repo root. generate_en_full.py builds the full English mirror into /en/.
- Both generators hardcode their output path as ~/workspace/bouyonmusique.com (the SITE variable at the top of each file). Clone the repo to that path, or edit SITE before running.
- Content lives in data_*.py modules: French module + matching *_en.py module. New content goes in a new module pair, registered in the import lists of generate.py and generate_en_full.py.
- After editing: run `python3 generate.py && python3 generate_en_full.py`, verify (no duplicate titles, no broken internal links, sitemap.xml lists every indexable page on disk except 404.html), commit, push, then check the live pages (GitHub Pages takes about 2 minutes).
- The root pages index.html, histoire/histories and artistes are hand-built, not generator-driven. Everything else comes from the modules.
- Read TAKEOVER-PLAN-20261020.md in this folder for the strategy. Content and style rules are in the handoff prompt Sean provides; they are strict (verified facts only, no copied text, no em dashes anywhere).
