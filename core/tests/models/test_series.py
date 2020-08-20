from django.core.exceptions import ValidationError
from django.test import TestCase

import core.strings as strings
from core.models import Series


class SeriesTestCase(TestCase):
    def setUp(self):
        Series.objects.create(name="Test 1")

    def test_url_is_generated(self):
        # Act.
        code = Series.objects.get(name="Test 1").url

        # Assert.
        self.assertEqual(len(code), strings.Constant.DEFAULT_CODE_LENGTH)

    def test_url_is_unique(self):
        # Arrange.
        code = Series.objects.get(name="Test 1").url

        # Act.
        series = Series(name="Test 2", url=code)

        # Assert.
        self.assertRaises(ValidationError, series.save)

    def test_url_is_same(self):
        # Arrange.
        series = Series.objects.get(name="Test 1")
        code = series.url

        # Act.
        series.name = "Test 2"
        series.save()

        # Assert.
        self.assertEqual(code, Series.objects.get(name="Test 2").url)
