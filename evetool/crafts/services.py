from crafts.models import Category, Group, Item, Blueprint, InputProduction, Invention, InputInvention
from django.core.exceptions import ObjectDoesNotExist
from crafts.calculator import Calculator
from config import PROTECTIVE_COMPONENTS, FROM_REACTION, TRIGLAVAN_COMPONENTS, CAPITAUX, SUBCAP, COST_INDEX, DECRYPTORS_LIST

class Services():

    def make_list(self, form):
        """main function for home view"""
        self.data = form.cleaned_data
        self.industry_dict = {}
        self.read_components()
        self.read_reaction()
        self.read_items()
        return self.industry_dict

    def read_components(self):
        """list all components selected items"""
        for component in self.data["composant"]:
            if component == "Protective":
                for compo in PROTECTIVE_COMPONENTS:
                    item = Item.objects.get(name=compo)
                    self.get_stats(item.name)
            else:
                items = Item.objects.filter(group_belong__name=component)
                for item in items:
                    if item.name in PROTECTIVE_COMPONENTS or item.name in TRIGLAVAN_COMPONENTS:
                        continue
                    else:
                        self.get_stats(item.name)

    def read_reaction(self):
        """list all reactions selected items"""
        for reaction in self.data["reaction"]:
            items = Item.objects.filter(group_belong__name=reaction)
            for item in items:
                self.get_stats(item.name)

    def read_items(self):
        """list all items selected"""
        for category in self.data["items"]:
            if category == "Subcap":
                items = Item.objects.filter(group_belong__category_belong__name="Ship")
                for item in items:
                    if item.group_belong.name in SUBCAP:
                        try:
                            bp = item.result.get()
                            if int(bp.time_prod) < 500:
                            #filter special edition ships
                                continue
                            if bp.tech_2:
                            #filter T2 ships
                                continue
                            else:
                                self.get_stats(item.name)
                        except ObjectDoesNotExist:
                            pass
                    else:
                        continue
            elif category == "Capital":
                items = Item.objects.filter(group_belong__category_belong__name="Ship")
                for item in items:
                    if item.group_belong.name in CAPITAUX:
                        try:
                            bp = item.result.get()
                            if int(bp.time_prod) < 500:
                                continue
                            if bp.tech_2:
                                continue
                            else:
                                self.get_stats(item.name)
                        except ObjectDoesNotExist:
                            pass
                    else:
                        continue
            else:
                items = Item.objects.filter(group_belong__category_belong__name=category)
                for item in items:
                    try:
                        bp = item.result.get()
                        if bp.tech_2:
                            self.get_stats(item.name)
                    except ObjectDoesNotExist:
                        pass

    def get_stats(self, name):
        """save item's stats"""
        loaded = self.load_data(name)
        calculator = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        stats = calculator.give_benef(loaded["components"])
        if stats["DAY_PROFIT_WEEK"] != "ERROR WITH MARKET DATA":
            self.industry_dict[name] = stats

    def load_data(self, name):
        """read blueprint to prepare some datas"""
        blueprint = Blueprint.objects.get(items_produced__name=name)
        components = self.item_data(blueprint)
        if blueprint.tech_2:
            compo_researched = self.invention_data(blueprint, components)
            if compo_researched != "Error with market":
                components = compo_researched
        return {
            "runs_per_day": 86400 / ( blueprint.time_prod * float(self.data["TE"]) ),
            "blueprint": blueprint,
            "components": components
        }

    def item_data(self, bp):
        """get components depending on arborescence"""
        data = self.prod_data(bp)
        if self.data["arborescence"] == '0':
            return data
        else:
            while self.check_material_only(data) == False:
                data = self.craft_detail(data)
            return data

    def prod_data(self, bp):
        """return components's list"""
        data = {}
        for item in bp.items_needed.all():
            if bp.tech_2:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( composants.quantity * 0.98 * float(self.data["item_t2_structures"]) * float(self.data["item_t2_rigg"]) ) / bp.quantity_produced
            elif bp.reaction:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( composants.quantity * float(self.data["reaction_structures"]) * float(self.data["reaction_rigg"]) ) / bp.quantity_produced
            else:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( ( composants.quantity * float(self.data["ME"]) * float(self.data["item_t1_structures"]) * float(self.data["item_t1_rigg"]) ) / bp.quantity_produced )
        return data

    def check_material_only(self, compo):
        """verify if item can be craft"""
        for key in compo.keys():
            item = Item.objects.get(name=key)
            if item.group_belong.name == "Fuel Block":
                if self.data["fuel_block"] == False:
                    continue  
            if self.data["arborescence"] == '1':
                if item.group_belong.name in FROM_REACTION:
                    continue
            try:
                Blueprint.objects.get(items_produced__name=key)
                return False
            except ObjectDoesNotExist:
                pass
        return True

    def craft_detail(self, data):
        """add components on components dict"""
        detail = {}
        for key, value in data.items():
            item = Item.objects.get(name=key)
            if item.group_belong.name == "Fuel Block":
                if self.data["fuel_block"] == False:
                    if key in detail:
                        detail[key] = detail[key] + value
                    else:
                        detail[key] = value
                    continue
            if self.data["arborescence"] == '1':
                if item.group_belong.name in FROM_REACTION:
                    if key in detail:
                        detail[key] = detail[key] + value
                    else:
                        detail[key] = value
                    continue
            try:
                bp = Blueprint.objects.get(items_produced__name=key)
                craft = self.prod_data(bp)
                for key2, value2 in craft.items():
                    if key2 in detail:
                        detail[key2] = detail[key2] + value2 * value
                    else:
                        detail[key2] = value2 * value
            except ObjectDoesNotExist:
                if key in detail:
                    detail[key] = detail[key] + value
                else:
                    detail[key] = value
        return detail

    def invention_data(self, bp, compo):
        """simulate components depending on decryptor"""
        bp_data = self.get_bp_data(bp, compo)
        if bp_data == "Error with market":
            return bp_data
        decryptor_data = self.without_decryptor(bp_data)
        if self.data["decryptor"] == "0":
            for decryptor in DECRYPTORS_LIST:
                with_decryptor = self.decryptor_bonus(bp_data, decryptor)
                if with_decryptor["total"] < decryptor_data["total"]:
                    decryptor_data = with_decryptor
        return decryptor_data["composants"]

    def get_bp_data(self, bp, compo):
        """init invention data + components data"""
        input_value = 0
        for key, value in compo.items():
            try:
                item = Item.objects.get(name=key)
                if item.week0_value is None:
                    return "Error with market"
                else:
                    input_value += float(item.week0_value) * float(value)
            except ObjectDoesNotExist:
                print("ERROR WITH DECRYPTOR FOR", key)
        bp_invention = Invention.objects.get(output_blueprint=bp)
        chance = float(bp_invention.succes_rate) * ( 1 + (( int(self.data["science1"]) + int(self.data["science2"]) ) / 30 ) + int(self.data['encryption']) / 40 )
        datacores = InputInvention.objects.filter(inventions=bp_invention)
        bp_data = {
            "blueprint": bp,
            "input_value": input_value,
            "chance": chance,
            "datacores": datacores,
            "composants": compo
        }
        return bp_data

    def without_decryptor(self, bp_data):
        """calcul componant without decryptor"""
        no_decryptor_compo = {}
        no_decryptor_total = bp_data["input_value"]
        for datacore in bp_data["datacores"]:
            no_decryptor_compo[datacore.items.name] = (( datacore.quantity / bp_data["chance"] ) / bp_data["blueprint"].quantity_produced )
            try:
                item = Item.objects.get(name=datacore.items.name)
                no_decryptor_total += float(item.week0_value) * float(datacore.quantity)
            except ObjectDoesNotExist:
                print("ERROR WITH DECRYPTOR FOR", datacore.items.name)
        for key, value in bp_data["composants"].items():
            no_decryptor_compo[key] = value
        without_decryptor = {
            "total": no_decryptor_total,
            "composants": no_decryptor_compo
        }
        return without_decryptor

    def decryptor_bonus(self, bp_data, decryptor_data):
        """calcul componant with decryptor"""
        total = 0
        data = {}
        decryptor = Item.objects.get(name=decryptor_data["Name"])
        for core in bp_data["datacores"]:
            data[core.items.name] = (( core.quantity / bp_data["chance"] * decryptor_data["Probability"] ) / bp_data["blueprint"].quantity_produced ) / ( 1 + decryptor_data["Add Run"])
        for key, value in data.items():
            try:
                item = Item.objects.get(name=key)
                total += float(item.week0_value) * float(value)
            except ObjectDoesNotExist:
                print("ERROR WITH DECRYPTOR FOR", item.name)
        total += ( bp_data["input_value"] * (( 100 - decryptor_data["Add ME"] ) / 100 )) + float(decryptor.week0_value)
        data[decryptor.name] = (( 1 / bp_data["chance"] * decryptor_data["Probability"] ) / bp_data["blueprint"].quantity_produced ) / ( 1 + decryptor_data["Add Run"])
        for key, value in bp_data["composants"].items():
            data[key] = value * (( 100 - decryptor_data["Add ME"] ) / 100 )
        return {"total": total, "composants": data}

    def show_info(self, data):
        """main functon for info view"""
        self.data = data["form"].cleaned_data
        loaded = self.load_data(data["item"])
        calculator = Calculator(loaded["blueprint"], loaded["runs_per_day"])
        return calculator.give_info(loaded["components"])
