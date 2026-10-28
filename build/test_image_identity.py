import contextlib
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import images


class ImageIdentity(unittest.TestCase):
    def test_pinned_source_replaces_cached_namesake_without_network(self):
        source_root = Path(images.ROOT)
        override = images._load(images.OVERRIDES, {})['kenny-g-dominica']
        with tempfile.TemporaryDirectory() as temp, contextlib.ExitStack() as stack:
            root = Path(temp)
            image = root / override['local_image']
            image.parent.mkdir(parents=True)
            image.write_bytes((source_root / override['local_image']).read_bytes())
            data = root / 'images.json'
            data.write_text(json.dumps({'kenny-g-dominica': {'source': {'kind': 'deezer', 'id': 523}}}))
            overrides = root / 'overrides.json'
            overrides.write_text(json.dumps({'kenny-g-dominica': override}))
            stack.enter_context(patch.multiple(images, ROOT=str(root), IMG_DIR=str(root/'img'),
                DATA=str(data), OVERRIDES=str(overrides), LISTEN=str(root/'missing'), YT_META=str(root/'missing')))
            stack.enter_context(patch.object(images, 'artists', return_value={'kenny-g-dominica':'Kenny G'}))
            stack.enter_context(patch.object(images, 'fetch', side_effect=AssertionError('Pinned image must not fetch a namesake')))
            images.gather()
            result = json.loads(data.read_text())['kenny-g-dominica']
            self.assertEqual(result['source'], override['source'])
            self.assertEqual(result['revision'], override['revision'])
            before = data.read_bytes()
            images.gather()
            self.assertEqual(before, data.read_bytes())
            image.write_bytes(b'wrong portrait')
            with self.assertRaisesRegex(ValueError, 'Pinned artist image changed'):
                images.gather(only={'kenny-g-dominica'})


if __name__ == '__main__':
    unittest.main()
