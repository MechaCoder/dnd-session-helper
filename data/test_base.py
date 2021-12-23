from unittest import TestCase
from data.base import projectRoot, dsfile, BaseData, BaseGetSet

class Test_projectRoot(TestCase):

    def test_one(self):

        obj = projectRoot()
        self.assertIsInstance(
            obj,
            str
        )

        self.assertEquals(
            obj[-1],
            'r'
        )

        self.assertEquals(
            obj[0],
            '/'
        )

class Test_dsfile(TestCase):

    def test_one(self):

        obj = dsfile()
        self.assertIsInstance(
            obj,
            str
        )

        self.assertEquals(
            obj[0],
            '/'
        )

        self.assertEquals(
            obj[-4:],
            'json'
        )

class Test_BaseData(TestCase):

    def test_init(self):

        obj = BaseData()

        self.assertEquals(
            obj.fileName,
            dsfile()
            
        )

        self.assertEquals(
            obj.table,
            'BaseData'
        )


    def test_readDoc_ids(self):

        obj = BaseData()

        self.assertIsInstance(
            obj.readDoc_ids(),
            list
        )

class Test_BaseGetSet(TestCase):

    def test_init(self):

        obj = BaseGetSet()
        self.assertIsInstance(
            obj.fileName,
            str
        )

