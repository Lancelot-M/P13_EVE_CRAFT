"""Testing services file"""

import pytest
import json
from pytest_django.asserts import assertTemplateUsed, assertContains
from django.test import Client
from django.test import TestCase
from crafts.forms import CraftForm

class TestViews(TestCase):
    """test views's file"""
    fixtures = ["dump.json"]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_home_get(self):

        form = CraftForm()
        client = Client()
        response = client.get('')
        assert response.status_code == 200
        assertTemplateUsed(response, "crafts/research.html")
        
    def test_home_post(self):

        client = Client()
        response = client.post("", data={
            'reaction': ["Hybrid Polymers"],
            'composant': [],
            'items': [],
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '0',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        })
        assert response.status_code == 200
        assertTemplateUsed(response, "crafts/research.html")
        assertContains(response, "C3-FTM Acid")
