from django.core.exceptions import ValidationError
from django.test import TestCase

import core.strings as strings
from core.models import Tag


class TagTestCase(TestCase):
    def setUp(self):
        Tag.objects.create(name="Test 1")

    def test_url_is_generated(self):
        # Act.
        code = Tag.objects.get(name="Test 1").url

        # Assert.
        self.assertEqual(len(code), strings.Constant.DEFAULT_CODE_LENGTH)

    def test_url_is_unique(self):
        # Arrange.
        code = Tag.objects.get(name="Test 1").url

        # Act.
        tag = Tag(name="Test 2", url=code)

        # Assert.
        self.assertRaises(ValidationError, tag.save)

    def test_url_is_same(self):
        # Arrange.
        tag = Tag.objects.get(name="Test 1")
        code = tag.url

        # Act.
        tag.name = "Test 2"
        tag.save()

        # Assert.
        self.assertEqual(code, Tag.objects.get(name="Test 2").url)
