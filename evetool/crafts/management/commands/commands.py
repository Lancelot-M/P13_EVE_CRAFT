import requests
import json
import yaml
from crafts.models import Category, Group, Item, Blueprint, InputProduction, Invention, InputInvention
from django.core.exceptions import ObjectDoesNotExist

class CreateDb():
    """class used to create the db"""
    #bp_category = "9"

    def create_db(self):
        """main function"""
        # self.init_categories()
        # self.init_items()
        # self.init_blueprints()
        # self.init_production_data()
        # self.set_t2_bool()
        self.detail_compo()

    def init_categories(self):
        """init categories and groups data"""
        items_categories = [2, 4, 6, 7, 8, 9, 17, 18, 22, 35, 43]
        for category_id in items_categories:
            url = "https://esi.evetech.net/latest/universe/categories/{}"
            params = {
            "datasource": "tranquility"
            }
            response = requests.get(url=url.format(category_id), params=params)
            try:
                response = response.json()
                try:
                    category_data = Category.objects.get(name=response["name"], categories_id=category_id)
                    print(response["name"], "ALREADY IN DATABASE")
                except ObjectDoesNotExist:
                    category_data = Category(name=response["name"], categories_id=category_id)
                    category_data.save()
                for group in response["groups"]:
                    url = "https://esi.evetech.net/latest/universe/groups/{}"
                    params = {
                    "datasource": "tranquility"
                    }
                    response2 = requests.get(url=url.format(group), params=params)
                    response2 = response2.json()
                    try:
                        group_data = Group.objects.get(name=response2["name"])
                        print(response2["name"], "ALREADY IN DATABASE")
                    except ObjectDoesNotExist:
                        group_data = Group(name=response2["name"], groups_id=group,
                                       category_belong=category_data)
                        group_data.save()
            except:
                print("!!!!!!!!!!!!!!!!!!!")

    def init_items(self):
        """init items datas"""
        groups = Group.objects.exclude(category_belong__categories_id=9)
        for group in groups:
            url = "https://esi.evetech.net/latest/universe/groups/{}"
            params = {
            "datasource": "tranquility"
            }
            response = requests.get(url=url.format(group.groups_id), params=params)
            response = response.json()
            for item in response["types"]:
                url = "https://esi.evetech.net/latest/universe/types/{}"
                params = {
                "datasource": "tranquility"
                }
                response2 = requests.get(url=url.format(item), params=params)
                try:
                    response2 = response2.json()
                    try:
                        item_data = Item.objects.get(name=response2["name"])
                    except ObjectDoesNotExist:
                        item_data = Item(name=response2["name"], types_id=response2["type_id"],
                                         group_belong=group)
                        item_data.save()
                        print(response2["name"], "ADDED IN DATABASE")
                except:
                    print("!!!!!!!!!!!!!!!!!!")

    def init_blueprints(self):
        """init bp name/id not the relations"""
        groups = Group.objects.filter(category_belong__categories_id=9)
        for group in groups:
            url = "https://esi.evetech.net/latest/universe/groups/{}"
            params = {
            "datasource": "tranquility"
            }
            response = requests.get(url=url.format(group.groups_id), params=params)
            try:
                response = response.json()
                for item in response["types"]:
                    url = "https://esi.evetech.net/latest/universe/types/{}"
                    params = {
                    "datasource": "tranquility"
                    }
                    response2 = requests.get(url=url.format(item), params=params)
                    try:
                        response2 = response2.json()
                        try:
                            blueprint = Blueprint.objects.get(name=response2["name"])
                            #print(blueprint.name, "ALREADY EXIST")
                        except ObjectDoesNotExist:
                            blueprint = Blueprint(name=response2["name"], types_id=response2["type_id"],
                                             group_belong=group)
                            blueprint.save()
                            print("______________", blueprint.name, "ADDED TO DATABASE _____________")
                    except:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            except:
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def filter_sde(self, sde):
        sde_check = {}
        for key, value in sde.items():
            if self.check_tags(value):
                sde_check[key] = value
        return sde_check

    def check_tags(self, value):
        if "activities" not in value:
            return False
        if "invention" in value["activities"]:
            if self.check_invention_tags(value["activities"]["invention"]) == 1:
                return False
        if "manufacturing" in value["activities"]:
            for tag in ["materials", "products", "time"]:
                if tag not in value["activities"]['manufacturing']:
                    return False
        if "reaction" in value["activities"]:
            for tag in ["materials", "products", "time"]:
                if tag not in value["activities"]["reaction"]:
                    return False
        return True

    def check_invention_tags(self, invention_data):
        for tag in ["materials", "products", "time"]:
            if tag not in invention_data:
                return 1
        for product in invention_data["products"]:
            for tag in ["probability", "quantity"]:
                if tag not in product:
                    return 1
        return 0

    def init_production_data(self):
        """init InputProduction + add bp field"""
        with open("crafts/management/commands/blueprints.yaml", "r") as f:
            try:
                f = yaml.safe_load(f)
                f = self.filter_sde(f)
                for key, value in f.items():
                    try:
                        blueprint = Blueprint.objects.get(types_id=key)
                        for key2, value2 in value["activities"].items():
                            #CRAFTING PART
                            if key2 == "reaction" or key2 == "manufacturing":
                                for material in value2["materials"]:
                                    try:
                                        item = Item.objects.get(types_id=material["typeID"])
                                        try:
                                            bp_input = InputProduction.objects.get(items=item, blueprints=blueprint)
                                        except ObjectDoesNotExist:
                                            bp_input = InputProduction(items=item, blueprints=blueprint,
                                                                     quantity=material["quantity"])
                                            bp_input.save()
                                            print("InputProduction  >>>", bp_input.items.name)
                                    except:
                                        pass
                                        #print(blueprint.name, "material not in db >>> ", material)
                                for product in value2["products"]:
                                    try:
                                        item = Item.objects.get(types_id=product["typeID"])
                                        try:
                                            check = Blueprint.objects.get(items_produced=item)
                                            check.quantity_produced = product["quantity"]
                                            check.save()
                                        except ObjectDoesNotExist:
                                            blueprint.items_produced = item
                                            blueprint.quantity_produced = product["quantity"]
                                            blueprint.save()
                                            print(blueprint.items_produced.name, "added to db")
                                    except ObjectDoesNotExist:
                                        pass
                                        #print("item ______", product["typeID"], "______ not in database")
                                blueprint.time_prod = value2["time"]
                            #INVENTION
                            if key2 == "invention":
                                for product in value2["products"]:
                                    try:
                                        bp_t2 = Blueprint.objects.get(types_id=product["typeID"])
                                        try:
                                            invention_data = Invention.objects.get(input_blueprint=blueprint, output_blueprint=bp_t2)
                                        except ObjectDoesNotExist:
                                            invention_data = Invention(input_blueprint=blueprint, output_blueprint=bp_t2,
                                                                        time=value2["time"], run_per_success=product["quantity"],
                                                                        succes_rate=product["probability"])
                                            invention_data.save()
                                            print(bp_t2, "ADDED TO DB")
                                            for material in value2["materials"]:
                                                try:
                                                    datacore = Item.objects.get(types_id=material["typeID"])
                                                    try:
                                                        check = Invention.objects.get(items_needed=datacore, input_blueprint=blueprint)
                                                        print("Datacore already added to relation")
                                                    except ObjectDoesNotExist:
                                                        research = InputInvention(items=datacore, inventions=invention_data, quantity=material["quantity"])
                                                        research.save()
                                                except:
                                                    print("datacore", product["typeID"], "not in database")
                                    except ObjectDoesNotExist:
                                        print(">>>>>>>>>   BP T2 NOT IN DATABASE     <<<<<<")
                    except ObjectDoesNotExist:
                        print("BLUEPRINT", key, "ISN'T IN DATABASE !!!!!!!!!!!!!")
            except yaml.YAMLError as exc:
                print(exc)

    def set_t2_bool(self):
        """configure tech_2 field in Blueprint"""
        inventions = Invention.objects.all()
        for invention in inventions:
            bp_t2 = Blueprint.objects.get(name=invention.output_blueprint.name)
            print(bp_t2.name)
            bp_t2.tech_2 = True
            bp_t2.save()


    #-------------- FONCTION DE LECTURE / TEST  --------------------------

    def return_composants(self, bp):
        materials = ["Harvestable Cloud", "Moon Materials", "Mineral", 'Fuel Block', "Molecular-Forged Materials"]
        items = bp.items_needed.all()
        composants = []
        for item in items:
            if item.group_belong.name in materials or item.group_belong.category_belong.name == "Planetary Commodities":
                data = InputProduction.objects.get(items=item, blueprints=bp)
                composants.append({data.items.name: data.quantity})
            else:
                item_bp = Blueprint.objects.get(items_produced=item)
                composants.append(self.return_composants(item_bp))
        return composants

    def flatten(self, list_of_lists):
        if len(list_of_lists) == 0:
            return list_of_lists
        if isinstance(list_of_lists[0], list):
            return self.flatten(list_of_lists[0]) + self.flatten(list_of_lists[1:])
        return list_of_lists[:1] + self.flatten(list_of_lists[1:])

    def dict_compo(self, list_compo):
        composants = {}
        for element in list_compo:
            for key, value in element.items():
                if key in composants:
                    composants[key] += value
                else:
                    composants[key] = value
        return composants


    def detail_compo(self):
        """list composant for t2 bp"""
        
        # Group a garder
        # Construction Component Blueprints
        # Composite Reaction Formulas
        # Polymer Reaction Formulas
        # Biochemical Reaction Formulas
        # Molecular-Forged Reaction Formulas
        # UTILISATEUR SELECTIONNE MODE FULL ITEM T2 SHIP 
        
        # for item in items:
        # print(item.name >> rentabilité >>> evolution >>> volume >> volumen/group)
        # data = Blueprint.objects.filter(items_produced__group_belong__category_belong__name="Ship")
        # for bp in data:
        #     print(bp.name)
        # for bp in data:
        
        bp = Blueprint.objects.get(name="Stiletto Blueprint")
        composants = self.return_composants(bp)
        composants = self.flatten(composants)
        print(self.dict_compo(composants))
        # week0_output = bp.quantity_produced * bp.items_produced.week0_value
        # week1_output = bp.quantity_produced * bp.items_produced.week1_value
        # month0_output = bp.quantity_produced * bp.items_produced.month0_value
        # month1_output = bp.quantity_produced * bp.items_produced.month1_value
        # week_progress = week0_profit * 100 - week1_profit * 100
        # month_progress = month0_profit * 100 - month1_profit * 100
        # print(bp.name)

class CallMarket():

    def main(self):
        self.init_market_values()

    def week_data(self, week):
        average = 0
        volume = 0
        if len(week) == 7:
            for day in week:
                average += (day["average"] * day["volume"])
                volume += day["volume"]
            average = round(average / (volume), 2)
            volume = int(volume / 7)
            data = {"average": average, "volume": volume}
            return data
        return {"average": None, "volume": None}

    def month_data(self, month):
        average = 0
        volume = 0
        if len(month) == 30:
            for day in month:
                average += (day["average"] * day["volume"])
                volume += day["volume"]
            average = round(average / (volume), 2)
            volume = int(volume / 30)
            data = {"average": average, "volume": volume}
            return data
        return {"average": None, "volume": None}

    def init_market_values(self):
        
        all_items = Item.objects.all()
        for item in all_items:
            #THE_FORGE = 10000002
            url = "https://esi.evetech.net/latest/markets/10000002/history/"
            params = {
            "datasource": "tranquility",
            "type_id": item.types_id
            }
            response = requests.get(url=url, params=params)
            response = response.json()
            if type(response) is dict:
                continue
            else:
                market = self.week_data(response[-7:])
                item.week0_value = market["average"]
                item.weeK0_quantity = market["volume"]
                market = self.week_data(response[-14:-7])
                item.week1_value = market["average"]
                item.weeK1_quantity = market["volume"]
                market = self.month_data(response[-30:])
                item.month0_value = market["average"]
                item.month0_quantity = market["volume"]
                market = self.month_data(response[-60:-30])
                item.month1_value = market["average"]
                item.month1_quantity = market["volume"]
                item.save()


class DeleteData():
    """Clean all datas from db"""
    def clean_all(self):
        Blueprint.objects.all().delete()
        Item.objects.all().delete()
        Group.objects.all().delete()
        Category.objects.all().delete()