from unittest import TestCase
from faker import Faker
from data.campain import CampainData

class Test_Campaign(TestCase):

    def test_create(self):

        obj = CampainData()
        camp = obj.create(
            Faker().name(), 
            Faker().text()
        ),
        
        self.assertIsInstance(
            camp[0],
            int
        )

        obj.removeById(camp[0])
        
