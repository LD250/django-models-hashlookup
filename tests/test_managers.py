from django.db import models
from django.test import TestCase

from hashlookup.querysets import gen_hash

from models import HashLookupTestModel

TEST_URL = 'https://test.com/help/about/article?date=2016-02-14&tool=main&from=producthunt'

class HashLookupTestCase(TestCase):
    def setUp(self):
        HashLookupTestModel.objects.create(url=TEST_URL, url_hash=gen_hash(TEST_URL))

    def test_filter_queryset(self):
        queryset = HashLookupTestModel.objects.filter(url=TEST_URL)
        print queryset

