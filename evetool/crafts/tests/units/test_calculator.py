"""Testing services file"""

import pytest
from django.test import TestCase
from crafts.models import Blueprint
from crafts.calculator import Calculator

class TestCalculator(TestCase):
    fixtures = ["dump2.json"]

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
        assert calculator_test.week0 == 29999366.125052
        assert calculator_test.week1 == 30274536.503180005
        assert calculator_test.month0 == 31247424.711832006
        assert calculator_test.month1 == 30688776.798112

    def test_calcul_benef(self):
        
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
        assert calculator_test.stats == {'DAY_PROFIT_MONTH': -3376318.622534616, 'DAY_PROFIT_WEEK': -3513646.627778564}
        assert calculator_test.day_profit_week1 == -3194230.9041182906
        assert calculator_test.day_profit_month1 == -1126536.8177198607

    def test_calcul_progress(self):
        
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
        calculator_test.calcul_progress()
        assert calculator_test.stats == {
            'DAY_PROFIT_MONTH': -3376318.622534616,
            'DAY_PROFIT_WEEK': -3513646.627778564,
            'day_profit_month_progress': 199.7077920070443,
            'day_profit_week_progress': 9.999769373230151
            }

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
        assert calculator_test.stats == {
            'DAY_PROFIT_MONTH': -3376318.622534616,
            'DAY_PROFIT_WEEK': -3513646.627778564,
            'DAY_PROFIT_WEEK_PROGRESS': 9.999769373230151,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7077920070443,
            'compo_progress_month': 1.8203655277468442,
            'compo_progress_week': -0.9089168981962814,
            'product_progress_month': -8.484959533903469,
            'product_progress_week': -2.718347323808067,
            'volume_progress_month': -13.924050632911388,
            'volume_progress_week': -5.263157894736835
        }

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
        assert calculator_test.stats == {
            'DAY_PROFIT_MONTH': -3376318.622534616,
            'DAY_PROFIT_WEEK': -3513646.627778564,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7077920070443,
            'DAY_PROFIT_WEEK_PROGRESS': 9.999769373230151,
            'RUNS_DAY': 0.72,
            'VOLUME': 68.0,
            'compo_progress_month': 1.8203655277468442,
            'compo_progress_week': -0.9089168981962814,
            'compo_value_month': 31247424.711832006,
            'compo_value_week': 29999366.125052,
            'item_selected': 'Manticore',
            'list_components': {
                'Construction Blocks': 29.4,
                'Datacore - Caldari Starship Engineering': 6.666666666666667,
                'Datacore - Mechanical Engineering': 6.666666666666667,
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
            },
            'product_progress_month': -8.484959533903469,
            'product_progress_week': -2.718347323808067,
            'product_value_month': 68.0,
            'product_value_week': 28910313.72,
            'product_volume_week': 72.0,
            'volume_progress_month': -13.924050632911388,
            'volume_progress_week': -5.263157894736835
        }

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
        assert calculator_test.give_benef(loaded["components"]) == {
            'DAY_PROFIT_MONTH': -3376318.622534616,
            'DAY_PROFIT_WEEK': -3513646.627778564,
            'day_profit_month_progress': 199.7077920070443,
            'day_profit_week_progress': 9.999769373230151
        }

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
        assert calculator_test.give_info(loaded["components"]) == {
            'DAY_PROFIT_MONTH': -3376318.622534616,
            'DAY_PROFIT_WEEK': -3513646.627778564,
            'DAY_PROFIT_MONTH_PROGRESS': 199.7077920070443,
            'DAY_PROFIT_WEEK_PROGRESS': 9.999769373230151,
            'RUNS_DAY': 0.72,
            'VOLUME': 68.0,
            'compo_progress_month': 1.8203655277468442,
            'compo_progress_week': -0.9089168981962814,
            'compo_value_month': 31247424.711832006,
            'compo_value_week': 29999366.125052,
            'item_selected': 'Manticore',
            'list_components': {
                'Construction Blocks': 29.4,
                'Datacore - Caldari Starship Engineering': 6.666666666666667,
                'Datacore - Mechanical Engineering': 6.666666666666667,
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
            },
            'product_progress_month': -8.484959533903469,
            'product_progress_week': -2.718347323808067,
            'product_value_month': 68.0,
            'product_value_week': 28910313.72,
            'product_volume_week': 72.0,
            'volume_progress_month': -13.924050632911388,
            'volume_progress_week': -5.263157894736835
        }