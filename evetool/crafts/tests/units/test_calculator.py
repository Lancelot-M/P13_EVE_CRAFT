"""Testing services file"""

import pytest
from django.test import TestCase
from crafts.models import Blueprint
from crafts.calculator import Calculator

class TestCalculator(TestCase):
    fixtures = ["dump.json"]

    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_calcul_input_value(self):

        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
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
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        calculator_test.calcul_input_value(loaded["components"])
        assert calculator_test.week0 == pytest.approx(29999366.1, 0.1)
        assert calculator_test.week1 == pytest.approx(30274536.5, 0.1)
        assert calculator_test.month0 == pytest.approx(31247424.7, 0.1)
        assert calculator_test.month1 == pytest.approx(30688776.7, 0.1)

    def test_calcul_benef(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        ref = {
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
        calculator_test = Calculator(ref["blueprint"], ref["runs_per_day"])
        calculator_test.calcul_input_value(ref["components"])
        calculator_test.calcul_benef()
        assert calculator_test.stats == {'DAY_PROFIT_MONTH': pytest.approx(-3376318.6, 0.1), 'DAY_PROFIT_WEEK': pytest.approx(-3513646.6, 0.1)}
        assert calculator_test.day_profit_week1 == pytest.approx(-3194230.9, 0.1)
        assert calculator_test.day_profit_month1 == pytest.approx(-1126536.8, 0.1)

    def test_calcul_progress(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
            'runs_per_day': 0.72,
            'blueprint': blueprint,
            'components': {
                'Datacore - Mechanical Engineering': pytest.approx(6.6, 0.1),
                'Datacore - Caldari Starship Engineering': pytest.approx(6.6, 0.1),
                'Nonlinear Metamaterials': 470.4,
                'Fullerides': 646.8, 
                'Titanium Carbide': 19574.52,
                'Morphite': 37.24,
                'Phenolic Composites': pytest.approx(1146.6, 0.1),
                'Ferrogel': pytest.approx(44.0, 0.1),
                'Hypersynaptic Fibers': 117.6,
                'Construction Blocks': 29.4,
                'Tritanium': pytest.approx(31376.34, 0.1),
                'Pyerite': pytest.approx(5893.0, 0.1),
                'Mexallon': pytest.approx(2456.5, 0.1),
                'Isogen': pytest.approx(492.4, 0.1),
                'Nocxium': pytest.approx(1.05, 0.1),
                'Sylramic Fibers': 3366.3,
                'Fermionic Condensates': 11.76
            }
        }
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        calculator_test.calcul_input_value(loaded["components"])
        calculator_test.calcul_benef()
        calculator_test.calcul_progress()
        ref = {
            'DAY_PROFIT_MONTH': 19796771.5,
            'DAY_PROFIT_WEEK': 16982966.5,
            'day_profit_month_progress': -8.4,
            'day_profit_week_progress': -3.1,
            'runs_day': 0.72,
            'volume': 68.0
        }
        for key, value in calculator_test.stats.items():
            assert ref[key] == pytest.approx(value, 0.1)

    def test_calcul_info(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
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
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        calculator_test.calcul_input_value(loaded["components"])
        calculator_test.calcul_benef()
        calculator_test.calcul_info()
        ref = {
            'DAY_PROFIT_MONTH': -3376318.6,
            'DAY_PROFIT_WEEK': -3513646.6,
            'DAY_PROFIT_WEEK_PROGRESS': 9.9,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7,
            'compo_progress_month': 1.8,
            'compo_progress_week': -0.9,
            'product_progress_month': -8.4,
            'product_progress_week': -2.7,
            'volume_progress_month': -13.9,
            'volume_progress_week': -5.2
        }
        for key, value in calculator_test.stats.items():
            assert ref[key] == pytest.approx(value, 0.1)

    def test_more_info(self):
       
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
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
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        calculator_test.calcul_input_value(loaded["components"])
        calculator_test.calcul_benef()
        calculator_test.calcul_info()
        calculator_test.more_info(loaded["components"])
        ref = {
            'DAY_PROFIT_MONTH': -3376318.6,
            'DAY_PROFIT_WEEK': -3513646.6,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7,
            'DAY_PROFIT_WEEK_PROGRESS': 9.999769373230151,
            'RUNS_DAY': 0.7,
            'VOLUME': 68,
            'compo_progress_month': 1.8,
            'compo_progress_week': -0.9,
            'compo_value_month': 31247424.7,
            'compo_value_week': 29999366.1,
            'item_selected': 'Manticore',
            'list_components': {
                'Construction Blocks': 29.4,
                'Datacore - Caldari Starship Engineering': 6.6,
                'Datacore - Mechanical Engineering': 6.6,
                'Fermionic Condensates': 11.7,
                'Ferrogel': 44,
                'Fullerides': 646.8,
                'Hypersynaptic Fibers': 117.6,
                'Isogen': 492.4,
                'Mexallon': 2456.5,
                'Morphite': 37.2,
                'Nanotransistors': 470.4,
                'Nocxium': 1,
                'Nonlinear Metamaterials': 470.4,
                'Phenolic Composites': 1146.6,
                'Pyerite': 5893,
                'Sylramic Fibers': 3366.3,
                'Titanium Carbide': 19574.5,
                'Tritanium': 31376.3
            },
            'product_progress_month': -8.4,
            'product_progress_week': -2.7,
            'product_value_month': 30550573,
            'product_value_week': 28910313.7,
            'product_volume_week': 72,
            'product_volume_month': 72,
            'volume_progress_month': -13.9,
            'volume_progress_week': -5.2
        }
        
        for key, value in calculator_test.stats.items():
            if key == 'list_components':
                for key_compo, val_compo in value.items():
                    assert ref[key][key_compo] == pytest.approx(val_compo, 0.1)
            else:
                assert ref[key] == pytest.approx(value, 0.1)

    def test_give_benef(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
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
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        data = calculator_test.give_benef(loaded["components"])
        ref = {
            'DAY_PROFIT_MONTH': -3376318,
            'DAY_PROFIT_WEEK': -3513646,
            'day_profit_month_progress': 199.7,
            'day_profit_week_progress': 9.9,
            'runs_day': 0.72,
            'volume': 68.0
        }
        for key, value in data.items():
            assert ref[key] == pytest.approx(value, 0.1)

    def test_give_info(self):
        
        blueprint = Blueprint.objects.get(name="Manticore Blueprint")
        loaded = {
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
        calculator_test = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        data = calculator_test.give_info(loaded["components"])
        ref = {
            'DAY_PROFIT_MONTH': -3376318,
            'DAY_PROFIT_WEEK': -3513646,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7,
            'DAY_PROFIT_WEEK_PROGRESS': 9.9,
            'RUNS_DAY': 0.72,
            'VOLUME': 68.0,
            'compo_progress_month': 1.8,
            'compo_progress_week': -0.9,
            'compo_value_month': 31247424,
            'compo_value_week': 29999366,
            'item_selected': 'Manticore',
            'list_components': {
                'Construction Blocks': 29.4,
                'Datacore - Caldari Starship Engineering': 6.6,
                'Datacore - Mechanical Engineering': 6.6,
                'Fermionic Condensates': 11.7,
                'Ferrogel': 44,
                'Fullerides': 646.8,
                'Hypersynaptic Fibers': 117.6,
                'Isogen': 492.4,
                'Mexallon': 2456.5,
                'Morphite': 37.2,
                'Nanotransistors': 470.4,
                'Nocxium': 1,
                'Nonlinear Metamaterials': 470.4,
                'Phenolic Composites': 1146.6,
                'Pyerite': 5893,
                'Sylramic Fibers': 3366.3,
                'Titanium Carbide': 19574.5,
                'Tritanium': 31376.3
            },
            'product_progress_month': -8.4,
            'product_progress_week': -2.7,
            'product_value_month': 30550573,
            'product_value_week': 28910313.7,
            'product_volume_week': 72.0,
            'product_volume_month': 68.0,
            'volume_progress_month': -13.9,
            'volume_progress_week': -5.2
        }
        for key, value in calculator_test.stats.items():
            if key == 'list_components':
                for key_compo, val_compo in value.items():
                    assert ref[key][key_compo] == pytest.approx(val_compo, 0.1)
            else:
                assert ref[key] == pytest.approx(value, 0.1)             
                
                