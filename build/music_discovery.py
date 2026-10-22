"""Preserve the reviewed listening additions when topic pages are regenerated."""
from pathlib import Path
import json
import re

START='<!-- music-discovery:start -->'
END='<!-- music-discovery:end -->'

def apply_music_discovery(site_root):
    root=Path(site_root)
    blocks=json.loads(Path(__file__).with_name('music_discovery_blocks.json').read_text())
    for name,body in blocks.items():
        page=root/name
        if not page.is_file():
            continue
        text=page.read_text()
        block=START+'\n'+body+'\n'+END
        if START in text:
            text=re.sub(re.escape(START)+r'.*?'+re.escape(END),lambda _:block,text,flags=re.S)
        else:
            marker='<h2>Read next</h2>' if name.startswith('en/') else '<h2>À lire aussi</h2>'
            if name!='index.html' and marker in text:
                text=text.replace(marker,block+'\n'+marker,1)
            else:
                text=text.replace('</main>',block+'\n</main>',1)
        page.write_text(text)

if __name__=='__main__':
    import sys
    apply_music_discovery(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1])
