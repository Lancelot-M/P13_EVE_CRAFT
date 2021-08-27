"""Testing services file"""

import pytest
import json
from django.test import TestCase
from crafts.models import Blueprint, InputProduction, Invention, InputInvention
from crafts.services import Services
from crafts.models import Item
from crafts.forms import CraftForm

class TestServices(TestCase):
    fixtures = ["dump2.json"]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_prod_data(self):
        """function got an instance of blueprint"""
        service_test = Services()
        service_test.data = {'reaction': [], 'composant': [], 'items': ['Ship'], 'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '0', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        
        bp_tech2 = Blueprint.objects.get(name="Manticore Blueprint")
        bp_reaction = Blueprint.objects.get(name="Ferrogel Reaction Formula")
        bp_ship = Blueprint.objects.get(name="Kestrel Blueprint")
        assert service_test.prod_data(bp_tech2) == {'Scalar Capacitor Unit': 58.8, 'Morphite': 37.24, 'Magpulse Thruster': 29.4, 'Gravimetric Sensor Cluster': 58.8, 'Construction Blocks': 29.4, 'R.A.M.- Starship Tech': 2.94, 'Titanium Diborite Armor Plate': 294.0, 'Quantum Microprocessor': 176.4, 'Kestrel': 0.98, 'Sustained Shield Emitter': 14.7, 'Graviton Reactor Unit': 5.88}
        assert service_test.prod_data(bp_reaction) == {'Ferrofluid': 0.25, 'Hexite': 0.25, 'Hydrogen Fuel Block': 0.0125, 'Hyperflurite': 0.25, 'Prometium': 0.25}
        assert service_test.prod_data(bp_ship) == {'Tritanium': 32000.0, 'Pyerite': 6000.0, 'Mexallon': 2500.0, 'Isogen': 500.0}

    def test_check_material_only(self):
        
        data_full = {'Tritanium': 32000.0, 'Hydrogen Fuel Block': 0.0125, 'Ferrogel': 58.8, "Scandium Metallofullerene": 22, "Stress-Responding Neurolink Stabilizer": 0.5}
        data_mini = {'Tritanium': 32000.0}
        data_fuel = {'Tritanium': 32000.0, 'Hydrogen Fuel Block': 0.0125}
        data_reaction = {'Tritanium': 32000.0, 'Ferrogel': 58.8, "Scandium Metallofullerene": 22, "Stress-Responding Neurolink Stabilizer": 0.5}

        ProdNo_Arbo1 = Services()
        ProdNo_Arbo1.data = {'fuel_block': False, 'arborescence': '1'}
        assert ProdNo_Arbo1.check_material_only(data_full) == True
        assert ProdNo_Arbo1.check_material_only(data_mini) == True
        assert ProdNo_Arbo1.check_material_only(data_fuel) == True
        assert ProdNo_Arbo1.check_material_only(data_reaction) == True

        ProdYes_Arbo1 = Services()
        ProdYes_Arbo1.data = {'fuel_block': True, 'arborescence': '1'}
        assert ProdYes_Arbo1.check_material_only(data_full) == False
        assert ProdYes_Arbo1.check_material_only(data_mini) == True
        assert ProdYes_Arbo1.check_material_only(data_fuel) == False
        assert ProdYes_Arbo1.check_material_only(data_reaction) == True

        ProdNo_Arbo2 = Services()
        ProdNo_Arbo2.data = {'fuel_block': False, 'arborescence': '2'}
        assert ProdNo_Arbo2.check_material_only(data_full) == False
        assert ProdNo_Arbo2.check_material_only(data_mini) == True
        assert ProdNo_Arbo2.check_material_only(data_fuel) == True
        assert ProdNo_Arbo2.check_material_only(data_reaction) == False

        ProdYes_Arbo2 = Services()
        ProdYes_Arbo2.data = {'fuel_block': True, 'arborescence': '2'}
        assert ProdYes_Arbo2.check_material_only(data_full) == False
        assert ProdYes_Arbo2.check_material_only(data_mini) == True
        assert ProdYes_Arbo2.check_material_only(data_fuel) == False
        assert ProdYes_Arbo2.check_material_only(data_reaction) == False

    def test_craft_detail(self):

        compo = {'Tritanium': 32000.0, 'Hydrogen Fuel Block': 0.0125, 'Ferrogel': 58.8, "Kestrel": 1}

        ProdNo_Arbo1 = Services()
        ProdNo_Arbo1.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '1', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdNo_Arbo1.craft_detail(compo) == {'Tritanium': 64000.0, 'Hydrogen Fuel Block': 0.0125, 'Ferrogel': 58.8, 'Pyerite': 6000.0, 'Mexallon': 2500.0, 'Isogen': 500.0}

        ProdYes_Arbo1 = Services()
        ProdYes_Arbo1.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '1', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdYes_Arbo1.craft_detail(compo) == {'Tritanium': 64000.0, 'Robotics': 0.00031250000000000006, 'Enriched Uranium': 0.0012500000000000002, 'Mechanical Parts': 0.0012500000000000002, 'Coolant': 0.0028125000000000003, 'Strontium Clathrates': 0.00625, 'Oxygen': 0.006875000000000001, 'Heavy Water': 0.053125000000000006, 'Liquid Ozone': 0.109375, 'Hydrogen Isotopes': 0.140625, 'Ferrogel': 58.8, 'Pyerite': 6000.0, 'Mexallon': 2500.0, 'Isogen': 500.0}

        ProdNo_Arbo2 = Services()
        ProdNo_Arbo2.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdNo_Arbo2.craft_detail(compo) == {'Tritanium': 64000.0, 'Hydrogen Fuel Block': 0.7474999999999999, 'Hexite': 14.7, 'Hyperflurite': 14.7, 'Ferrofluid': 14.7, 'Prometium': 14.7, 'Pyerite': 6000.0, 'Mexallon': 2500.0, 'Isogen': 500.0}

        ProdYes_Arbo2 = Services()
        ProdYes_Arbo2.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdYes_Arbo2.craft_detail(compo) == {'Tritanium': 64000.0, 'Robotics': 0.00031250000000000006, 'Enriched Uranium': 0.0012500000000000002, 'Mechanical Parts': 0.0012500000000000002, 'Coolant': 0.0028125000000000003, 'Strontium Clathrates': 0.00625, 'Oxygen': 0.006875000000000001, 'Heavy Water': 0.053125000000000006, 'Liquid Ozone': 0.109375, 'Hydrogen Isotopes': 0.140625, 'Hydrogen Fuel Block': 0.735, 'Hexite': 14.7, 'Hyperflurite': 14.7, 'Ferrofluid': 14.7, 'Prometium': 14.7, 'Pyerite': 6000.0, 'Mexallon': 2500.0, 'Isogen': 500.0}

    def test_item_data(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        ProdNo_Arbo1 = Services()
        ProdNo_Arbo1.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '1', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdNo_Arbo1.item_data(blueprint) == {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }

        ProdYes_Arbo1 = Services()
        ProdYes_Arbo1.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '1', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdYes_Arbo1.item_data(blueprint) == {
            'Construction Blocks': 29.4,
            'Fermionic Condensates': 11.76,
            'Ferrogel': 44.099999999999994,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Pyerite': 5893.0536,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Tritanium': 31376.3464
        }

        ProdNo_Arbo2 = Services()
        ProdNo_Arbo2.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdNo_Arbo2.item_data(blueprint) == {
            'Atmospheric Gases': 15.68,
            'Cadmium': 37.45159090909091,
            'Caesium': 36.83909090909091,
            'Chromium': 217.6776,
            'Construction Blocks': 29.4,
            'Dysprosium': 94.6925,
            'Evaporite Deposits': 167.66419090909093,
            'Hafnium': 117.81159090909091,
            'Helium Fuel Block': 4.961250000000001,
            'Hydrocarbons': 10.78,
            'Hydrogen Fuel Block': 7.844454545454545,
            'Isogen': 492.4108,
            'Mercury': 26.46,
            'Mexallon': 2456.5268,
            'Morphite': 37.24,
            'Neodymium': 18.62,
            'Nitrogen Fuel Block': 14.546875,
            'Nocxium': 1.0584,
            'Oxygen Fuel Block': 30.59896318181818,
            'Platinum': 60.025,
            'Promethium': 13.964999999999998,
            'Pyerite': 5893.0536,
            'Silicates': 162.76419090909093,
            'Technetium': 26.46,
            'Thulium': 2.94,
            'Titanium': 176.2726,
            'Tritanium': 31376.3464,
            'Vanadium': 39.41159090909092
        }

        ProdYes_Arbo2 = Services()
        ProdYes_Arbo2.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        assert ProdYes_Arbo2.item_data(blueprint) == {
            'Atmospheric Gases': 15.68,
            'Cadmium': 37.45159090909091,
            'Caesium': 36.83909090909091,
            'Chromium': 217.6776,
            'Construction Blocks': 29.4,
            'Coolant': 13.039097113636364,
            'Dysprosium': 94.6925,
            'Enriched Uranium': 5.795154272727274,
            'Evaporite Deposits': 167.66419090909093,
            'Hafnium': 117.81159090909091,
            'Heavy Water': 246.2940565909091,
            'Helium Isotopes': 55.814062500000006,
            'Hydrocarbons': 10.78,
            'Hydrogen Isotopes': 88.25011363636364,
            'Isogen': 492.4108,
            'Liquid Ozone': 507.07599886363636,
            'Mechanical Parts': 5.795154272727274,
            'Mercury': 26.46,
            'Mexallon': 2456.5268,
            'Morphite': 37.24,
            'Neodymium': 18.62,
            'Nitrogen Isotopes': 163.65234375,
            'Nocxium': 1.0584,
            'Oxygen': 31.873348500000006,
            'Oxygen Isotopes': 344.23833579545453,
            'Platinum': 60.025,
            'Promethium': 13.964999999999998,
            'Pyerite': 5893.0536,
            'Robotics': 1.4487885681818184,
            'Silicates': 162.76419090909093,
            'Strontium Clathrates': 28.975771363636362,
            'Technetium': 26.46,
            'Thulium': 2.94,
            'Titanium': 176.2726,
            'Tritanium': 31376.3464,
            'Vanadium': 39.41159090909092
        }

    def test_get_bp_data(self):

        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        bp_invention = Invention.objects.get(output_blueprint=blueprint)
        datacores = InputInvention.objects.filter(inventions=bp_invention)
        service_test = Services()
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        components = {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }
        result_1 = service_test.get_bp_data(blueprint, components) 
        result_2 = {
            'blueprint': blueprint,
            'input_value': 28764699.925052, 
            'chance': 0.3,
            'datacores': datacores,
            "composants": components
        }

        assert result_1["blueprint"] == result_2["blueprint"]
        assert result_1["input_value"] == result_2["input_value"]
        assert result_1["chance"] == result_2["chance"]
        assert result_1["composants"] == result_2["composants"]
        x = 0
        for el in result_2["datacores"]:
            assert el == result_1["datacores"][x]
            x += 1

    def test_without_decryptor(self):

        service_test = Services()
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        components = {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }
        data_test = service_test.get_bp_data(blueprint, components)
        data_test = service_test.without_decryptor(data_test)
        assert data_test == {
            'total': 29135099.785051998,
            'composants': {
                'Datacore - Mechanical Engineering': 6.666666666666667,
                'Datacore - Caldari Starship Engineering': 6.666666666666667,
                'Construction Blocks': 29.4,
                'Fermionic Condensates': 11.76,
                'Fullerides': 646.8,
                'Hypersynaptic Fibers': 117.6,
                'Morphite': 37.24,
                'Nanotransistors': 470.4,
                'Nocxium': 1.0584,
                'Nonlinear Metamaterials': 470.4,
                'Phenolic Composites': 1146.6000000000001,
                'Sylramic Fibers': 3366.3,
                'Titanium Carbide': 19574.52,
                'Ferrogel': 44.099999999999994,
                'Isogen': 492.4108,
                'Mexallon': 2456.5268,
                'Pyerite': 5893.0536, 
                'Tritanium': 31376.3464
            }
        }

    def test_decryptor_bonus(self):

        service_test = Services()
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        components = {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }
        data_test = service_test.get_bp_data(blueprint, components)
        accelerant = {
            "Probability": 1.20,
            "Add Run": 1,
            "Add ME": 2,
            "Name": "Accelerant Decryptor"
        }
        assert service_test.decryptor_bonus(data_test, accelerant) == {
            'total': 29288912.936550956,
            'composants': {
                'Datacore - Mechanical Engineering': 4.0,
                'Datacore - Caldari Starship Engineering': 4.0,
                'Accelerant Decryptor': 2.0,
                'Construction Blocks': 28.811999999999998,
                'Fermionic Condensates': 11.524799999999999,
                'Fullerides': 633.8639999999999,
                'Hypersynaptic Fibers': 115.24799999999999,
                'Morphite': 36.495200000000004,
                'Nanotransistors': 460.99199999999996,
                'Nocxium': 1.037232,
                'Nonlinear Metamaterials': 460.99199999999996,
                'Phenolic Composites': 1123.6680000000001,
                'Sylramic Fibers': 3298.974,
                'Titanium Carbide': 19183.0296,
                'Ferrogel': 43.217999999999996,
                'Isogen': 482.56258399999996,
                'Mexallon': 2407.396264,
                'Pyerite': 5775.1925280000005,
                'Tritanium': 30748.819472
            }
        }

    def test_invention_data(self):

        service_test = Services()
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        components = {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }
        data_test = service_test.invention_data(blueprint, components)
        assert data_test == {
            'Datacore - Mechanical Engineering': 6.666666666666667,
            'Datacore - Caldari Starship Engineering': 6.666666666666667,
            'Construction Blocks': 29.4,
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.24,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0584,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6000000000001,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.52,
            'Ferrogel': 44.099999999999994,
            'Isogen': 492.4108,
            'Mexallon': 2456.5268,
            'Pyerite': 5893.0536,
            'Tritanium': 31376.3464
        }

    def test_load_data(self):

        service_test = Services()
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        assert service_test.load_data(name="Manticore") == {
            'runs_per_day': 0.72,
            'blueprint': blueprint,
            'components': {
                'Datacore - Mechanical Engineering': 6.666666666666667,
                'Datacore - Caldari Starship Engineering': 6.666666666666667,
                'Nanotransistors': 470.4,
                'Nonlinear Metamaterials': 470.4,
                'Fullerides': 646.8, 
                'Titanium Carbide': 19574.52,
                'Morphite': 37.24,
                'Phenolic Composites': 1146.6000000000001,
                'Ferrogel': 44.099999999999994,
                'Hypersynaptic Fibers': 117.6,
                'Construction Blocks': 29.4,
                'Tritanium': 31376.3464,
                'Pyerite': 5893.0536,
                'Mexallon': 2456.5268,
                'Isogen': 492.4108,
                'Nocxium': 1.0584,
                'Sylramic Fibers': 3366.3,
                'Fermionic Condensates': 11.76
            }
        }

    def test_get_stats(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        service_test.get_stats("Manticore")
        assert service_test.industry_dict == {
            'Manticore': {
                'DAY_PROFIT_WEEK': -3513646.627778564,
                'DAY_PROFIT_MONTH': -3376318.622534616,
                'day_profit_week_progress': 9.999769373230151,
                'day_profit_month_progress': 199.7077920070443
            }
        }

    def test_read_components(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': [],
            'composant': ["Protective", "Construction Components", "Capital Construction Components", "Hybrid Tech Components"],
            'items': ['Ship'],
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        service_test.read_components()
        with open("crafts/tests/units/read_components.json", "r") as f:
            data = json.load(f)
        assert service_test.industry_dict == data

    def test_read_reaction(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': ["Composite", "Hybrid Polymers", "Molecular-Forged Materials"],
            'composant': [],
            'items': ['Ship'],
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        service_test.read_reaction()
        with open("crafts/tests/units/read_reaction.json", "r") as f:
            data = json.load(f)
        assert service_test.industry_dict == data

    def test_read_items(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': ["Composite"],
            'composant': [],
            'items': ['Ship', "Subcap", "Capital", "Module", "Charge", "Drone"],
            'reaction_structures': '1',
            'reaction_rigg': '1',
            'item_t1_structures': '1',
            'item_t1_rigg': '1',
            'item_t2_structures': '1',
            'item_t2_rigg': '1',
            'fuel_block': False,
            'arborescence': '1',
            'ME': '1',
            'TE': '1',
            'science1': '0',
            'science2': '0',
            'encryption': '0',
            'decryptor': '0'
        }
        service_test.read_items()
        with open("crafts/tests/units/read_items.json", "r") as f:
            data = json.load(f)
        assert service_test.industry_dict == data

    def test_make_list(self):

        with open("crafts/tests/units/make_list.json", "r") as f:
            data = json.load(f)
        formulaire = CraftForm(data={
            'reaction': [],
            'composant': [],
            'items': ['Ship'],
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
        if formulaire.is_valid():
            service_test = Services()
            service_test.make_list(formulaire)
            assert service_test.industry_dict == data
        else:
            assert formulaire == ""

    def test_show_info(self):

        formulaire = CraftForm(data={
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
        if formulaire.is_valid():
            data = {
                "form": formulaire,
                "item": "Methanofullerene"
            }
            service_test = Services()
            with open("crafts/tests/units/show_info.json", "r") as f:
                result = json.load(f)
            assert service_test.show_info(data) == result
        else :
            assert formulaire == ""
