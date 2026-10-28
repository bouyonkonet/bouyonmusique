import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image, IptcImagePlugin
import images
import image_discovery as gallery


class GalleryLifecycle(unittest.TestCase):
    def test_publish_repeat_and_withdraw(self):
        original_root=Path(images.ROOT)
        d=json.loads(Path(images.DATA).read_text())['asa-bantan']
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); build=root/'build'; build.mkdir()
            (root/'en').mkdir(); (root/'img/artistes').mkdir(parents=True)
            for width in (640,1280):
                for ext in ('jpg','webp'):
                    rel=f'img/artistes/{d["file"]}-{width}.{ext}'
                    shutil.copyfile(original_root/rel,root/rel)
            for rel in ('asa-bantan.html','en/asa-bantan.html'):
                (root/rel).write_text('<html><main><p class="lead">Asa Bantan</p></main></html>')
            (root/'sitemap.xml').write_text('<sitemapindex></sitemapindex>')
            (build/'images.json').write_text(json.dumps({'asa-bantan':d}))
            (build/'rollout.json').write_text(json.dumps({'asa-bantan':'2026-10-28'}))
            with contextlib.ExitStack() as stack:
                stack.enter_context(patch.multiple(images,ROOT=str(root),DATA=str(build/'images.json'),ROLLOUT=str(build/'rollout.json'),OVERRIDES=str(build/'overrides.json')))
                stack.enter_context(patch.multiple(gallery,ROOT=root,MANIFEST=build/'manifest.json',CACHE=build/'cache.json'))
                images.apply_images(); gallery.apply_discovery()
                page=(root/'photos/asa-bantan.html').read_text()
                self.assertIn('Asa Bantan',page)
                self.assertEqual(len(list((root/'img/photos').glob('*'))),16)
                self.assertEqual((root/'sitemap-images.xml').read_text().count('<image:image>'),32)
                self.assertNotIn('acquireLicensePage',page)
                self.assertNotIn('"license":',page)
                jpeg=root/gallery.variant_path('asa-bantan',d,1280,'jpg','banner').lstrip('/')
                with Image.open(jpeg) as im:
                    self.assertEqual(im.size,(1280,720))
                    self.assertGreater(len(IptcImagePlugin.getiptcinfo(im)[(2,25)]),60)
                    self.assertIn('Asa Bantan',im.getexif()[0x9C9E].decode('utf-16-le'))
                def hashes():
                    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
                before=hashes(); images.apply_images(); gallery.apply_discovery()
                self.assertEqual(before,hashes(),'Repeat build must not change any output')
                (build/'overrides.json').write_text(json.dumps({'asa-bantan':{'skip':True}}))
                images.apply_images(); gallery.apply_discovery()
                self.assertFalse((root/'photos/asa-bantan.html').exists())
                self.assertFalse((root/'en/photos/asa-bantan.html').exists())
                self.assertEqual(list((root/'img/photos').glob('*')),[])
                self.assertNotIn('asa-bantan.html',(root/'sitemap-images.xml').read_text())
                self.assertNotIn('artist-hero',(root/'asa-bantan.html').read_text())
                self.assertNotIn('photos/asa-bantan.html',(root/'asa-bantan.html').read_text())


if __name__=='__main__':unittest.main()
