from unittest import TestCase
import shutil

import storage
from storage import (
    DuplicateException, drop_all, owner_to_id,
    create_owner, create_content, update_content, crupdate_content, get_content
)

# Change the path for db storage.
storage.init({'STORAGE_PATH': 'data/tests'})


class StorageTest(TestCase):
    def sample_owner(self):
        return create_owner(name='example.com')

    def sample_content(self, owner=None):
        owner = owner or self.sample_owner()
        return create_content(owner=owner, name='content', value='hey')

    def test_create_owner(self):
        owner = self.sample_owner()
        self.assertIsNotNone(owner)
        self.assertEqual(owner['name'], 'example.com')
        self.assertTrue(len(owner['key']) > 20)

    def test_owner_to_id(self):
        self.assertEqual(owner_to_id(5), 5)
        owner = create_owner(name='example.com')
        self.assertEqual(owner_to_id(owner), owner.eid)

    def test_create_owner_duplicate(self):
        owner = self.sample_owner()
        self.assertRaises(DuplicateException, create_owner, name=owner['name'])

    def test_create_content(self):
        owner = self.sample_owner()
        content = self.sample_content(owner=owner)
        self.assertIsNotNone(content)
        self.assertEqual(content['owner'], owner.eid)
        self.assertEqual(content['name'], 'content')
        self.assertEqual(content['value'], 'hey')

    def test_create_content_duplicate(self):
        content = self.sample_content()
        self.assertRaises(DuplicateException, create_content,
                          owner=content['owner'], name=content['name'],
                          value='unique')

    def test_update_content(self):
        content = self.sample_content()
        update_content(name=content['name'], owner=content['owner'],
                       value='updated value')
        # Retrieve from db to ensure the updated value is persistently saved.
        content = get_content(content['name'], content['owner'])
        self.assertEqual(content['value'], 'updated value')

    def test_crupdate_content(self):
        content = crupdate_content('mycontent', 'my value', 1)
        self.assertIsNotNone(content)
        self.assertEqual(content['value'], 'my value')
        content = crupdate_content('mycontent', 'updated', 1)
        self.assertEqual(content['value'], 'updated')

    def tearDown(self):
        drop_all()
