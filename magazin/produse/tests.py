from django.test import TestCase

# Create your tests here.
from produse.models import Produse


class EntryTestCase(TestCase):
    def setUp(self):
        """Crearea de produse"""
        Produse.objects.create(nume='ciorapi',
                               marca='Andreaua SA',
                               descriere='ciorapi ieftini',
                               pret=5.3,
                               stoc=10)

    def test_if_entry_exists(self):
        """testarea crearii"""
        intrare = Produse.objects.get(nume="ciorapi")
        print(intrare.nume, intrare.marca, intrare.descriere)
        self.assertEqual(intrare.nume, 'ciorapi')
        self.assertEqual(intrare.pret, 5.3)