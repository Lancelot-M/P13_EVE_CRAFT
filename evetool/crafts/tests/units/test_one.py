"""Testing services file"""

import pytest
import json
from django.test import TestCase
from crafts.models import Blueprint, InputProduction, Invention, InputInvention
from crafts.services import Services
from crafts.models import Item
from crafts.forms import CraftForm

class TestServices(TestCase):
    fixtures = ["dump.json"]

    @classmethod
    def setUpTestData(cls):
        pass

    def test_prod_data(self):
        """function got an instance of blueprint"""
        service_test = Services()
        service_test.data = {
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
        }
        
        bp_tech2 = Blueprint.objects.get(name="Manticore Blueprint")
        bp_reaction = Blueprint.objects.get(name="Ferrogel Reaction Formula")
        bp_ship = Blueprint.objects.get(name="Kestrel Blueprint")
        assert service_test.prod_data(bp_tech2) == {
            'Scalar Capacitor Unit': 58.8,
            'Morphite': 37.24,
            'Magpulse Thruster': 29.4,
            'Gravimetric Sensor Cluster': 58.8,
            'Construction Blocks': 29.4,
            'R.A.M.- Starship Tech': 2.94,
            'Titanium Diborite Armor Plate': 294.0,
            'Quantum Microprocessor': 176.4,
            'Kestrel': 0.98,
            'Sustained Shield Emitter': 14.7,
            'Graviton Reactor Unit': 5.88
        }
        assert service_test.prod_data(bp_reaction) == {
            'Ferrofluid': 0.25,
            'Hexite': 0.25,
            'Hydrogen Fuel Block': 0.0125,
            'Hyperflurite': 0.25,
            'Prometium': 0.25
        }
        assert service_test.prod_data(bp_ship) == {
            'Tritanium': 32000.0,
            'Pyerite': 6000.0,
            'Mexallon': 2500.0,
            'Isogen': 500.0
        }

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
        assert ProdNo_Arbo1.craft_detail(compo) == {
            'Tritanium': 64000.0,
            'Hydrogen Fuel Block': 0.0125,
            'Ferrogel': 58.8,
            'Pyerite': 6000.0,
            'Mexallon': 2500.0,
            'Isogen': 500.0
        }

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
        reference = {
            'Construction Blocks': 29.4,          
            'Fermionic Condensates': 11.76,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.2,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.5,
            'Ferrogel': 44.0,
            'Isogen': 492.4,
            'Mexallon': 2456.5,
            'Pyerite': 5893.0,
            'Tritanium': 31376.3
        }
        data = ProdNo_Arbo1.item_data(blueprint)
        for key, value in data.items():
            assert reference[key] == pytest.approx(value, 0.1)

        ProdYes_Arbo2 = Services()
        ProdYes_Arbo2.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '1', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        reference = {
            'Construction Blocks': 29.4,
            'Fermionic Condensates': 11.7,
            'Ferrogel': 44.0,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Isogen': 492.4,
            'Mexallon': 2456.5,
            'Morphite': 37.2,
            'Nanotransistors': 470.4,
            'Nocxium': 1.0,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6,
            'Pyerite': 5893.0,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.5,
            'Tritanium': 31376.3
        }
        data = ProdYes_Arbo2.item_data(blueprint)
        for key, value in data.items():
            assert reference[key] == pytest.approx(value, 0.1)

        ProdNo_Arbo3 = Services()
        ProdNo_Arbo3.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': False, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        reference = {
            'Atmospheric Gases': 15.6,
            'Cadmium': 37.4,
            'Caesium': 36.8,
            'Chromium': 217.6,
            'Construction Blocks': 29.4,
            'Dysprosium': 94.6,
            'Evaporite Deposits': 167.6,
            'Hafnium': 117.8,
            'Helium Fuel Block': 4.9,
            'Hydrocarbons': 10.7,
            'Hydrogen Fuel Block': 7.8,
            'Isogen': 492.4,
            'Mercury': 26.4,
            'Mexallon': 2456.5,
            'Morphite': 37.2,
            'Neodymium': 18.6,
            'Nitrogen Fuel Block': 14.5,
            'Nocxium': 1.0,
            'Oxygen Fuel Block': 30.5,
            'Platinum': 60,
            'Promethium': 13.9,
            'Pyerite': 5893.0,
            'Silicates': 162.7,
            'Technetium': 26.4,
            'Thulium': 2.9,
            'Titanium': 176.2,
            'Tritanium': 31376.3,
            'Vanadium': 39.4
        }
        data = ProdNo_Arbo3.item_data(blueprint)
        for key, value in data.items():
            assert reference[key] == pytest.approx(value, 0.1)

        ProdYes_Arbo4 = Services()
        ProdYes_Arbo4.data = {'reaction_structures': '1', 'reaction_rigg': '1', 'item_t1_structures': '1', 'item_t1_rigg': '1', 'item_t2_structures': '1', 'item_t2_rigg': '1', 'fuel_block': True, 'arborescence': '2', 'ME': '1', 'TE': '1', 'science1': '0', 'science2': '0', 'encryption': '0', 'decryptor': '0'}
        reference = {
            'Atmospheric Gases': 15.6,
            'Cadmium': 37.4,
            'Caesium': 36.8,
            'Chromium': 217.6,
            'Construction Blocks': 29.4,
            'Coolant': 13.0,
            'Dysprosium': 94.6,
            'Enriched Uranium': 5.7,
            'Evaporite Deposits': 167.6,
            'Hafnium': 117.8,
            'Heavy Water': 246.2,
            'Helium Isotopes': 55.8,
            'Hydrocarbons': 10.7,
            'Hydrogen Isotopes': 88.2,
            'Isogen': 492.4,
            'Liquid Ozone': 507.0,
            'Mechanical Parts': 5.7,
            'Mercury': 26.4,
            'Mexallon': 2456.5,
            'Morphite': 37.2,
            'Neodymium': 18.6,
            'Nitrogen Isotopes': 163.6,
            'Nocxium': 1.0,
            'Oxygen': 31.8,
            'Oxygen Isotopes': 344.2,
            'Platinum': 60.0,
            'Promethium': 13.9,
            'Pyerite': 5893.0,
            'Robotics': 1.4,
            'Silicates': 162.7,
            'Strontium Clathrates': 28.9,
            'Technetium': 26.4,
            'Thulium': 2.9,
            'Titanium': 176.2,
            'Tritanium': 31376.3,
            'Vanadium': 39.4
        }
        data = ProdYes_Arbo4.item_data(blueprint)
        for key, value in data.items():
            assert reference[key] == pytest.approx(value, 0.1)

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
            'Fermionic Condensates': 11.7,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.2,
            'Nanotransistors': 470.4,
            'Nocxium': 1,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.5,
            'Ferrogel': 44,
            'Isogen': 492.4,
            'Mexallon': 2456.5,
            'Pyerite': 5893,
            'Tritanium': 31376.3
        }
        result_1 = service_test.get_bp_data(blueprint, components) 
        result_2 = {
            'blueprint': blueprint,
            'input_value': 28764699, 
            'chance': 0.3,
            'datacores': datacores,
            "composants": components
        }

        assert result_1["blueprint"] == result_2["blueprint"]
        assert pytest.approx(result_1["input_value"], 0.1) == result_2["input_value"]
        assert result_1["chance"] == result_2["chance"]
        for key, value in result_1["composants"].items():
            assert result_2["composants"][key] == pytest.approx(value, 0.1)
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
        data = service_test.get_bp_data(blueprint, components)
        data = service_test.without_decryptor(data)
        reference = {
            'total': 29135099,
            'composants': {
                'Datacore - Mechanical Engineering': 6.6,
                'Datacore - Caldari Starship Engineering': 6.6,
                'Construction Blocks': 29.4,
                'Fermionic Condensates': 11.7,
                'Fullerides': 646.8,
                'Hypersynaptic Fibers': 117.6,
                'Morphite': 37.2,
                'Nanotransistors': 470.4,
                'Nocxium': 1,
                'Nonlinear Metamaterials': 470.4,
                'Phenolic Composites': 1146.6,
                'Sylramic Fibers': 3366.3,
                'Titanium Carbide': 19574.5,
                'Ferrogel': 44,
                'Isogen': 492.4,
                'Mexallon': 2456.5,
                'Pyerite': 5893, 
                'Tritanium': 31376.3
            }
        }
        assert reference["total"] == pytest.approx(data["total"], 0.1)
        for key, value in data["composants"].items():
            assert reference["composants"][key] == pytest.approx(value, 0.1)

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
        bonus = service_test.decryptor_bonus(data_test, accelerant)
        assert bonus["total"] == pytest.approx(29288912)
        assert bonus["composants"]["Datacore - Mechanical Engineering"] == 4.0
        assert bonus["composants"]['Datacore - Caldari Starship Engineering'] == 4.0
        assert bonus["composants"]['Accelerant Decryptor'] == pytest.approx(1.3, 0.1)
        assert bonus["composants"]['Construction Blocks'] == pytest.approx(28.8, 0.1)
        assert bonus["composants"]['Fermionic Condensates'] == pytest.approx(11.5, 0.1)
        assert bonus["composants"]['Fullerides'] == pytest.approx(633.8, 0.1)
        assert bonus["composants"]['Hypersynaptic Fibers'] == pytest.approx(115.2, 0.1)
        assert bonus["composants"]['Morphite'] == pytest.approx(36.4, 0.1)
        assert bonus["composants"]['Nanotransistors'] == pytest.approx(460.9, 0.1)
        assert bonus["composants"]['Nocxium'] == pytest.approx(1.0, 0.1)
        assert bonus["composants"]['Nonlinear Metamaterials'] == pytest.approx(460.9, 0.1)
        assert bonus["composants"]['Phenolic Composites'] == pytest.approx(1123.6, 0.1)
        assert bonus["composants"]['Sylramic Fibers'] == pytest.approx(3298.9, 0.1)
        assert bonus["composants"]['Titanium Carbide'] == pytest.approx(19183, 0.1)
        assert bonus["composants"]['Ferrogel'] == pytest.approx(43.2, 0.1)
        assert bonus["composants"]['Isogen'] == pytest.approx(482.5, 0.1)
        assert bonus["composants"]['Mexallon'] == pytest.approx(2407.3, 0.1)
        assert bonus["composants"]['Pyerite'] == pytest.approx(5775.1, 0.1)
        assert bonus["composants"]['Tritanium'] == pytest.approx(30748.8, 0.1)

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
        data = service_test.invention_data(blueprint, components)
        reference = {
            'Datacore - Mechanical Engineering': 6.6,
            'Datacore - Caldari Starship Engineering': 6.6,
            'Construction Blocks': 29.4,
            'Fermionic Condensates': 11.7,
            'Fullerides': 646.8,
            'Hypersynaptic Fibers': 117.6,
            'Morphite': 37.2,
            'Nanotransistors': 470.4,
            'Nocxium': 1,
            'Nonlinear Metamaterials': 470.4,
            'Phenolic Composites': 1146.6,
            'Sylramic Fibers': 3366.3,
            'Titanium Carbide': 19574.5,
            'Ferrogel': 44,
            'Isogen': 492.4,
            'Mexallon': 2456.5,
            'Pyerite': 5893,
            'Tritanium': 31376.3
        }
        for key, value in data.items():
            assert reference[key] == pytest.approx(value, 0.1)

    def test_load_data(self):

        dico = {
            'Datacore - Mechanical Engineering': 6.6,
            'Datacore - Caldari Starship Engineering': 6.6,
            'Nanotransistors': 470.4,
            'Nonlinear Metamaterials': 470.4,
            'Fullerides': 646.8, 
            'Titanium Carbide': 19574.5,
            'Morphite': 37.2,
            'Phenolic Composites': 1146.6,
            'Ferrogel': 44.0,
            'Hypersynaptic Fibers': 117.6,
            'Construction Blocks': 29.4,
            'Tritanium': 31376.3,
            'Pyerite': 5893.0,
            'Mexallon': 2456.5,
            'Isogen': 492.4,
            'Nocxium': 1.0,
            'Sylramic Fibers': 3366.3,
            'Fermionic Condensates': 11.7
        }
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
        data = service_test.load_data(name="Manticore")
        for key, value in data["components"].items():
            assert dico[key] == pytest.approx(value, 0.1)
        assert data["blueprint"] == blueprint
        assert data["runs_per_day"] == 0.72

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
        ship = service_test.industry_dict["Manticore"]
        assert ship["DAY_PROFIT_WEEK"] == pytest.approx(-3513646)
        assert ship['DAY_PROFIT_MONTH'] == pytest.approx(-3376318)
        assert ship['day_profit_week_progress'] == pytest.approx(9.9, 0.1)
        assert ship ['day_profit_month_progress'] == pytest.approx(199.7, 0.1)

    def test_read_components(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': [],
            'composant': ["Protective", "Construction Components"],
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
        for key, value in service_test.industry_dict.items():
            for key2, value2 in value.items():
                assert data[key][key2] == pytest.approx(value2, 0.1)

    def test_read_reaction(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': ["Composite", "Molecular-Forged Materials"],
            'composant': [],
            'items': ["Capital"],
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
        for key, value in service_test.industry_dict.items():
            for key2, value2 in value.items():
                assert data[key][key2] == pytest.approx(value2, 0.1)

    def test_read_items(self):

        service_test = Services()
        service_test.industry_dict = {}
        service_test.data = {
            'reaction': ["Composite"],
            'composant': [],
            'items': ["Ship"],
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
            'science1': '4',
            'science2': '0',
            'encryption': '3',
            'decryptor': '0'
        }
        service_test.read_items()
        with open("crafts/tests/units/read_items.json", "r") as f:
            data = json.load(f)
        for key, value in service_test.industry_dict.items():
            for key2, value2 in value.items():
                assert data[key][key2] == pytest.approx(value2, 0.1)

    def test_make_list(self):

        
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
            with open("crafts/tests/units/make_list.json", "r") as f:
                data = json.load(f)
            for key, value in service_test.industry_dict.items():
                for key2, value2 in value.items():
                    assert data[key][key2] == pytest.approx(value2, 0.1)
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
            data = service_test.show_info(data)
            with open("crafts/tests/units/show_info.json", "r") as f:
                reference = json.load(f)
            for key, value in data.items():
                if value is type(dict):
                    for key2, value2 in value.items():
                        assert reference[key][key2] == pytest.approx(value2, 0.1)
                else:
                    assert reference[key] == pytest.approx(value, 0.1)
        else :
            assert formulaire == ""
