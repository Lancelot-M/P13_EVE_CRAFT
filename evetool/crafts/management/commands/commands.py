import requests
import json
import yaml
from crafts.models import Category, Group, Item, Blueprint, InputProduction, Invention, InputInvention
from django.core.exceptions import ObjectDoesNotExist
from config import PROTECTIVE_COMPONENTS, FROM_REACTION
from django.db.models import Q

class CreateDb():
    """class used to create the db"""
    #bp_category = "9"

    def create_db(self):
        """main function"""
        self.init_groups()
        self.init_items()
        self.init_blueprints()
        self.init_production_data()
        self.set_t2_bool()
        self.clean_old_data()

    def init_groups(self):
        """init categories and groups data"""
        items_categories = [4, 6, 7, 8, 9, 17, 18, 35, 43, 87]
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
                print('problem with category', category_id, "request")
        
        #Create group Harvestable CLoud in Category 2
        url = "https://esi.evetech.net/latest/universe/groups/711"
        params = {
        "datasource": "tranquility"
        }
        response = requests.get(url=url, params=params)
        response = response.json()
        try:
            group_data = Group.objects.get(name=response["name"])
            print(response["name"], "ALREADY IN DATABASE")
        except ObjectDoesNotExist:
            category_data = Category(name="Celestial", categories_id=2)
            category_data.save()
            group_data = Group(name=response["name"], groups_id=response["group_id"],
                           category_belong=category_data)
            group_data.save()

        print("-------------------------- GROUPS DOWNLOADED   ----------------------------------")
        print("")
        print("")

    def init_items(self):
        """init items datas"""
        groups = Group.objects.all()
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
                            item_data = Item.objects.get(name=response2["name"])
                            print(item_data.name, "already in db")
                        except ObjectDoesNotExist:
                            item_data = Item(name=response2["name"], types_id=response2["type_id"],
                                             group_belong=group)
                            item_data.save()
                    except:
                        print("problem with", item, "request")
            except:
                print("problem with item call request :", group.name)
        print("-------------------- ITEMS DOWNLOADED --------------------------")
        print("")
        print("")

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
                            print(blueprint.name, "ALREADY EXIST")
                        except ObjectDoesNotExist:
                            blueprint = Blueprint(name=response2["name"], types_id=response2["type_id"],
                                             group_belong=group)
                            blueprint.save()
                    except:
                        print("problem with", item, "request")
            except:
                print("problem with", group, "request")
        print("  ---------------------  BLUEPRINTS DOWNLOADED   ----------------------------")
        print("")
        print("")

    def filter_sde(self, sde):

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
                            if key2 == "manufacturing":
                                for material in value2["materials"]:
                                    try:
                                        item = Item.objects.get(types_id=material["typeID"])
                                        try:
                                            bp_input = InputProduction.objects.get(items=item, blueprints=blueprint)
                                        except ObjectDoesNotExist:
                                            bp_input = InputProduction(items=item, blueprints=blueprint,
                                                                     quantity=material["quantity"])
                                            bp_input.save()
                                    except:
                                        # print(blueprint.name, "material not in db >>> ", material)
                                        pass
                                for product in value2["products"]:
                                    try:
                                        item = Item.objects.get(types_id=product["typeID"])
                                        bp = Blueprint.objects.filter(items_produced__name=item.name)
                                        if bp:
                                            print("ERROR WITH",item.name, "ONE BP ALREADY SAVED")
                                            continue
                                        blueprint.items_produced = item
                                        blueprint.quantity_produced = product["quantity"]
                                        blueprint.save()
                                    except ObjectDoesNotExist:
                                        # print(blueprint.name, "product not in db >>> ", product)
                                        pass
                                blueprint.time_prod = value2["time"]
                                blueprint.save()
                            #REACTION PART
                            if key2 == "reaction":
                                for material in value2["materials"]:
                                    try:
                                        item = Item.objects.get(types_id=material["typeID"])
                                        try:
                                            bp_input = InputProduction.objects.get(items=item, blueprints=blueprint)
                                        except ObjectDoesNotExist:
                                            bp_input = InputProduction(items=item, blueprints=blueprint,
                                                                     quantity=material["quantity"])
                                            bp_input.save()
                                    except:
                                        # print(blueprint.name, "material not in db >>> ", material)
                                        pass
                                for product in value2["products"]:
                                    try:
                                        item = Item.objects.get(types_id=product["typeID"])
                                        bp = Blueprint.objects.filter(items_produced__name=item.name)
                                        if bp:
                                            print("ERROR WITH",item.name, "ONE BP ALREADY SAVED")
                                            continue
                                        blueprint.items_produced = item
                                        blueprint.quantity_produced = product["quantity"]
                                        blueprint.save()
                                    except ObjectDoesNotExist:
                                        # print(blueprint.name, "product not in db >>> ", product)
                                        pass
                                blueprint.time_prod = value2["time"]
                                blueprint.reaction = True
                                blueprint.save()
                            #INVENTION PART
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
                                            for material in value2["materials"]:
                                                try:
                                                    datacore = Item.objects.get(types_id=material["typeID"])
                                                    research = InputInvention(items=datacore, inventions=invention_data, quantity=material["quantity"])
                                                    research.save()
                                                except:
                                                    # print("datacore", product["typeID"], "not in database")
                                                    pass
                                    except ObjectDoesNotExist:
                                        print(key, ">>>>>>>>>   bp t2 not in database    <<<<<<")
                    except ObjectDoesNotExist:
                        # print("BLUEPRINT", key, "ISN'T IN DATABASE !!!!!!!!!!!!!")
                        pass
            except yaml.YAMLError as exc:
                print(exc)
        print("-------------------------  BLUEPRINTS SET -------------------------------")

    def set_t2_bool(self):
        """configure tech_2 field in Blueprint"""
        inventions = Invention.objects.all()
        for invention in inventions:
            bp_t2 = Blueprint.objects.get(name=invention.output_blueprint.name)
            bp_t2.tech_2 = True
            bp_t2.save()
        print("----------------  BP T2 SET   ---------------")

    def clean_old_data(self):

        old_data = {}
        bp = Blueprint.objects.all()
        for el in bp:
            if el.tech_2 == True:
                data = Invention.objects.filter(output_blueprint=el)
                if len(data) > 1:
                    bug_bp = []
                    for bug in data:
                        bug_bp.append(bug)
                    old_data[el.name] = bug_bp
        for key, value in old_data.items():
            try:
                bp = Blueprint.objects.get(name=key)
                bp.delete()
            except:
                print(key, "doens't exist")
            for el in value:
                try:
                    bp = Blueprint.objects.get(name=el)
                    bp.delete()
                except:
                    print(el, "doesn't exist")
        Item.objects.get(name="Venerable").delete()
        Item.objects.get(name="Vanguard").delete()


class Industry():

    # INFO :
    # Job cost = Estimated items value × System cost index × Structure bonuses
    # Tax cost = Job cost × Tax%

    def start_industry(self):
        """Function to quick access in local"""
        print("HELPER COMMAND")


class CallMarket():

    def main(self):
        self.init_market_values()
        while self.call_status():
           self.init_market_values()
        call_failed = []
        call_done = []
        with open("crafts/management/commands/items_already_called.json", "w") as f:
            f.write(json.dumps(call_failed, indent=4, sort_keys=True,
                               ensure_ascii=False))
        with open("crafts/management/commands/items_call_failed.json", "w") as f:
            f.write(json.dumps(call_done, indent=4, sort_keys=True,
                               ensure_ascii=False))
        print("-------- MARKET DATA DOWNLOADED --------------")

    def call_status(self):
        with open("crafts/management/commands/items_call_failed.json", "r") as f:
            already_call = json.load(f)   
            if len(already_call) == 0:
                return 0
            return 1

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
        
        with open("crafts/management/commands/items_not_callable.json", "r") as f:
            not_collable = json.load(f)
        with open("crafts/management/commands/items_already_called.json", "r") as f:
            already_call = json.load(f)
        with open("crafts/management/commands/items_call_failed.json", "r") as f:
            failed_call = json.load(f)

        all_items = Item.objects.all()
        for item in all_items:
            if item.name in not_collable or item.name in already_call:
                continue
            else:
                #THE_FORGE = 10000002
                url = "https://esi.evetech.net/latest/markets/10000002/history/"
                params = {
                "datasource": "tranquility",
                "type_id": item.types_id
                }
                request = requests.get(url=url, params=params)
                if request.status_code == 200:
                    try:
                        response = request.json()
                        market0 = self.week_data(response[-7:])
                        item.week0_value = market0["average"]
                        item.week0_quantity = market0["volume"]  
                        market1 = self.week_data(response[-14:-7])
                        item.week1_value = market1["average"]
                        item.week1_quantity = market1["volume"]   
                        market2 = self.month_data(response[-30:])
                        item.month0_value = market2["average"]
                        item.month0_quantity = market2["volume"]          
                        market3 = self.month_data(response[-60:-30])
                        item.month1_value = market3["average"]
                        item.month1_quantity = market3["volume"]
                        item.save()
                        print(item.name, "SAVED")
                        already_call.append(item.name)
                    except:
                        print("ERROR WITH >>>", item.name, "<<< REQUEST")
                elif request.status_code == 400 or request.status_code == 404:
                    not_collable.append(item.name)
                elif request.status_code == 504:
                    print("failed_call", request.status_code)
                    failed_call.append(item.name)
                else:
                    print("ERROR:", request.status_code, 'with :', item.name)
        with open("crafts/management/commands/items_not_callable.json", "w") as f:
            f.write(json.dumps(not_collable, indent=4, sort_keys=True,
                               ensure_ascii=False))
        with open("crafts/management/commands/items_already_called.json", "w") as f:
            f.write(json.dumps(already_call, indent=4, sort_keys=True,
                               ensure_ascii=False))
        with open("crafts/management/commands/items_call_failed.json", "w") as f:
            f.write(json.dumps(failed_call, indent=4, sort_keys=True,
                               ensure_ascii=False))
        print("__________________")
        print(failed_call)


class DeleteData():
    """Clean all datas from db"""
    def clean_all(self):
        Blueprint.objects.all().delete()
        Item.objects.all().delete()
        Group.objects.all().delete()
        Category.objects.all().delete()