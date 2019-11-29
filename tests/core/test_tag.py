from unittest import TestCase

from GTG.core.tag import Tag


class TestTag(TestCase):
    def setUp(self):
        self.tag = Tag('foo', None)
        # Do not allow notifying related tasks
        self.tag.notify_related_tasks = lambda: None

    def test_has_name(self):
        self.assertEqual('foo', self.tag.get_name())

    def test_name_is_attribute(self):
        self.assertEqual('foo', self.tag.get_attribute('name'))

    def test_missing_attribute_returns_none(self):
        self.assertEqual(None, self.tag.get_attribute('no-such-attribute'))

    def test_set_then_get_attribute(self):
        self.tag.set_attribute('new-attribute', 'value')
        attr = self.tag.get_attribute('new-attribute')
        self.assertEqual('value', attr)

    def test_set_non_str_attribute_casts_to_string(self):
        self.tag.set_attribute('new-attribute', 42)
        attr = self.tag.get_attribute('new-attribute')
        self.assertEqual('42', attr)

    def test_initial_attribute_is_name_only(self):
        self.assertEqual(['name'], self.tag.get_all_attributes())

    def test_can_add_new_attributes(self):
        self.tag.set_attribute('bar', 'baz')
        self.assertEqual({'name', 'bar'}, set(self.tag.get_all_attributes()))

    def test_get_all_attributes_but_name(self):
        self.assertEqual([], self.tag.get_all_attributes(butname=True))
        self.tag.set_attribute('bar', 'baz')
        self.assertEqual(['bar'], self.tag.get_all_attributes(butname=True))

    def test_name_cannot_be_changed(self):
        self.assertEqual('foo', self.tag.get_name())

        with self.assertRaises(KeyError):
            self.tag.set_attribute('name', 'new')

        self.assertEqual('foo', self.tag.get_name())
        self.assertEqual('foo', self.tag.get_attribute('name'))
