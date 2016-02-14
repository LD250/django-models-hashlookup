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
        sql_with_params = queryset.query.sql_with_params()
        #(u'SELECT "tests_hashlookuptestmodel"."id", "tests_hashlookuptestmodel"."url", "tests_hashlookuptestmodel"."url_hash" FROM "tests_hashlookuptestmodel" WHERE "tests_hashlookuptestmodel"."url" = %s', ('https://test.com/help/about/article?date=2016-02-14&tool=main&from=producthunt',))
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(sql_with_params[1][0], TEST_URL)
        self.assertIn('"tests_hashlookuptestmodel"."url" = %s', sql_with_params[0])

    def test_filter_queryset_hash(self):
        queryset = HashLookupTestModel.objects_hash.filter(url=TEST_URL)
        sql_with_params = queryset.query.sql_with_params()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(sql_with_params[1][0], gen_hash(TEST_URL))
        self.assertIn('"tests_hashlookuptestmodel"."url_hash" = %s', sql_with_params[0])

    def test_filter_queryset_hash_contains(self):
        queryset = HashLookupTestModel.objects_hash.filter(url__contains='test.com')
        sql_with_params = queryset.query.sql_with_params()
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(sql_with_params[1][0], "%test.com%")
        self.assertIn('"tests_hashlookuptestmodel"."url" LIKE %s', sql_with_params[0])

