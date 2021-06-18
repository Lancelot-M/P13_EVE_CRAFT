from crafts.models import Category, Group, Item, Blueprint, InputProduction, Invention, InputInvention
from django.core.exceptions import ObjectDoesNotExist
from config import PROTECTIVE_COMPONENTS, FROM_REACTION, TRIGLAVAN_COMPONENTS, CAPITAUX, SUBCAP

class Services():

    def make_list(self, form):
        
        self.data = form.cleaned_data
        self.t2_ME = 0.98
        self.t2_TE = 0.96
        self.cost_index = 1.015

        industry_dict = {}

        for component in self.data["composant"]:
            if component == "Protective":
                for compo in PROTECTIVE_COMPONENTS:
                    item = Item.objects.get(name=compo)
                    print(item.name)
                    stats = self.calcul_benef(item.name)
                    if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                        continue
                    industry_dict[item.name] = stats
            else:
                items = Item.objects.filter(group_belong__name=component)
                for item in items:
                    if item.name in PROTECTIVE_COMPONENTS or item.name in TRIGLAVAN_COMPONENTS:
                        continue
                    else:
                        print(item.name)
                        stats = self.calcul_benef(item.name)
                        if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                            continue
                        industry_dict[item.name] = stats

        for reaction in self.data["reaction"]:
            items = Item.objects.filter(group_belong__name=reaction)
            for item in items:
                print(item.name)
                stats = self.calcul_benef(item.name)
                if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                    continue
                industry_dict[item.name] = stats

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
                                print(item.name)
                                stats = self.calcul_benef(item.name)
                                if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                                    continue
                                industry_dict[item.name] = stats
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
                            #filter special edition ships
                                continue
                            if bp.tech_2:
                            #filter T2 ships
                                continue
                            else:
                                print(item.name)
                                stats = self.calcul_benef(item.name)
                                if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                                    continue
                                industry_dict[item.name] = stats
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
                            print(item.name)
                            stats = self.calcul_benef(item.name)
                            if stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA":
                                continue
                            industry_dict[item.name] = stats
                    except ObjectDoesNotExist:
                        pass

        return industry_dict

        
    def show_info(self, data):

        self.data = data["form"].cleaned_data
        self.t2_ME = 1
        self.t2_TE = 0.96
        self.cost_index = 1.015

        info = self.info_detail(data["item"])
        return info
   

    def info_detail(self, name):

        bp = Blueprint.objects.get(items_produced__name=name)
        data = self.item_data(bp)
        print(data)
        product = bp.items_produced
        bp_run_day = 86400 / ( bp.time_prod * float(self.data["TE"]) )
        
        compo_value_week0 = 0
        compo_value_week1 = 0
        compo_value_month0 = 0
        compo_value_month1 = 0

        try:
            for key, value in data.items():
                item = Item.objects.get(name=key)
                price = float(item.week0_value) * float(value)
                compo_value_week0 += price
                price = float(item.week1_value) * float(value)
                compo_value_week1 += price
                price = float(item.month0_value) * float(value)
                compo_value_month0 += price
                price = float(item.month1_value) * float(value)
                compo_value_month1 += price
        except TypeError:
            # MARKET DATA ERROR USUALLY ITEM NOT IN MARKET
            pass
        try:
            week0_benef = float(product.week0_value) * 0.95 - ( compo_value_week0 * self.cost_index )
            day_profit_week0 = ( week0_benef * bp.quantity_produced ) * bp_run_day
        except TypeError:
            week0_benef = 0.00
            day_profit_week0 = "ERROR WITH MARKET DATA"
        try:
            week1_benef = float(product.week1_value) * 0.95 - compo_value_week1 * self.cost_index
            day_profit_week1 = ( week1_benef * bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_week1 = "ERROR WITH MARKET DATA"
            
        try:
            month0_benef = float(product.month0_value) * 0.95 - compo_value_month0 * self.cost_index
            day_profit_month0 = ( month0_benef * bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_month0 = "ERROR WITH MARKET DATA"           
        try:
            month1_benef = float(product.month1_value) * 0.95 - compo_value_month1 * self.cost_index
            day_profit_month1 = ( month1_benef * bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_month1 = "ERROR WITH MARKET DATA"  
        
        
        if day_profit_week0 == "ERROR WITH MARKET DATA" or day_profit_week1 == "ERROR WITH MARKET DATA":
            week_progress = 0
            compo_week_progress = 0
            product_progress_week = 0
            volume_progress_week = 0
        else:
            week_progress = ( ( day_profit_week0 * 100 ) / day_profit_week1 ) - 100
            compo_week_progress = compo_value_week0 * 100 / compo_value_week1 - 100
            product_progress_week = product.week0_value * 100 / product.week1_value - 100
            volume_progress_week = product.week0_quantity * 100 / product.week1_quantity - 100
        
        if day_profit_month0 == "ERROR WITH MARKET DATA" or day_profit_month1 == "ERROR WITH MARKET DATA":
            month_progress = 0
            compo_month_progress = 0
            product_progress_month = 0
            volume_progress_month = 0
        else:
            month_progress = ( (day_profit_month0 * 100 ) / day_profit_month1 ) - 100
            compo_month_progress = compo_value_month0 * 100 / compo_value_month1 - 100
            product_progress_month = product.month0_value * 100 / product.month1_value - 100
            volume_progress_month = product.month0_quantity * 100 / product.month1_quantity - 100
            
        info = {
            "DAY_PROFIT_WEEK": day_profit_week0,
            "DAY_PROFIT_MONTH": day_profit_month0,
            "DAY_PROFIT_WEEK_PROGRESS": week_progress,
            "DAY_PROFIT_MONTH_PROGRESS": month_progress,
            "VOLUME": product.month0_quantity,
            "RUNS_DAY": bp_run_day * bp.quantity_produced,
            "compo_value_week": compo_value_week0,
            "compo_value_month": compo_value_month0,
            "compo_progress_week": compo_week_progress,
            "compo_progress_month": compo_month_progress,
            "product_value_week": product.week0_value,
            "product_value_month": product.month0_value,
            "product_progress_week": product_progress_week,
            "product_progress_month": product_progress_month,
            "product_volume_week": product.week0_quantity,
            "product_volume_month": product.month0_quantity,
            "volume_progress_week": volume_progress_week,
            "volume_progress_month": volume_progress_month,
            "list_components" : data,
            "item_selected": name
        }
        return info

    def calcul_benef(self, research):

        research_bp = Blueprint.objects.get(items_produced__name=research)
        data = self.item_data(research_bp)
        product = research_bp.items_produced
        bp_run_day = 86400 / ( research_bp.time_prod * float(self.data["TE"]) )
        week0 = 0
        week1 = 0
        month0 = 0
        month1 = 0

        try:
            for key, value in data.items():
                item = Item.objects.get(name=key)
                price = float(item.week0_value) * float(value)
                week0 += price
                price = float(item.week1_value) * float(value)
                week1 += price
                price = float(item.month0_value) * float(value)
                month0 += price
                price = float(item.month1_value) * float(value)
                month1 += price
        except TypeError:
            # MARKET DATA ERROR USUALLY ITEM NOT IN MARKET
            pass
        try:
            week0_benef = float(product.week0_value) * 0.95 - ( week0 * self.cost_index )
            day_profit_week0 = ( week0_benef * research_bp.quantity_produced ) * bp_run_day
        except TypeError:
            week0_benef = 0.00
            day_profit_week0 = "ERROR WITH MARKET DATA"
        try:
            week1_benef = float(product.week1_value) * 0.95 - week1 * self.cost_index
            day_profit_week1 = ( week1_benef * research_bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_week1 = "ERROR WITH MARKET DATA"
            
        try:
            month0_benef = float(product.month0_value) * 0.95- month0 * self.cost_index
            day_profit_month0 = ( month0_benef * research_bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_month0 = "ERROR WITH MARKET DATA"           
        try:
            month1_benef = float(product.month1_value) * 0.95 - month1 * self.cost_index
            day_profit_month1 = ( month1_benef * research_bp.quantity_produced ) * bp_run_day
        except TypeError:
            day_profit_month1 = "ERROR WITH MARKET DATA"  
        
        if day_profit_week0 == "ERROR WITH MARKET DATA" or day_profit_week1 == "ERROR WITH MARKET DATA":
            week_progress = "ERROR WITH MARKET DATA"
        else:
            week_progress = ( ( day_profit_week0 * 100 ) / day_profit_week1 ) - 100
        if day_profit_month0 == "ERROR WITH MARKET DATA" or day_profit_month1 == "ERROR WITH MARKET DATA":
            month_progress = "ERROR WITH MARKET DATA"
        else:
            month_progress = ( (day_profit_month0 * 100 ) / day_profit_month1 ) - 100
        
        stats = {
            "DAY_PROFIT_WEEK": day_profit_week0,
            "DAY_PROFIT_MONTH": day_profit_month0,
            "day_profit_week_progress": week_progress,
            "day_profit_month_progress": month_progress,
            "volume": product.month0_quantity,
            "runs_day": bp_run_day * research_bp.quantity_produced
        }
        return stats


    def item_data(self, bp):
        
        data = self.prod_data(bp)
        if self.data["arborescence"] == '0':
            return data
        else:
            while self.check_material_only(data) == False:
                data = self.craft_detail(data)
            return data

    def prod_data(self, bp):
    
        data = {}
        # if error
        # print(item)
        if bp.tech_2:
            datacore = self.invention_data(bp)
            for key, value in datacore.items():
                data[key] = value
        for item in bp.items_needed.all():
            if bp.tech_2:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( composants.quantity * self.t2_ME * float(self.data["item_t2_structures"]) * float(self.data["item_t2_rigg"]) ) / bp.quantity_produced
            elif bp.reaction:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( composants.quantity * float(self.data["reaction_structures"]) * float(self.data["reaction_rigg"]) ) / bp.quantity_produced
            else:
                composants = InputProduction.objects.get(items=item, blueprints=bp)
                data[item.name] = ( ( composants.quantity * float(self.data["ME"]) * float(self.data["item_t1_structures"]) * float(self.data["item_t1_rigg"]) ) / bp.quantity_produced )
        return data

    def invention_data(self, bp):
        
        # success_chance = BASE * ( 1 + ( Skill 1 + Skill 2 ) / 30 + Racial Skill / 40 ) * ( 1 + Decryptor / 100)
        data = {}
        bp_invention = Invention.objects.get(output_blueprint__name=bp.name)
        chance = float(bp_invention.succes_rate) * ( 1 + (( int(self.data["science1"]) + int(self.data["science2"]) ) / 30 ) + int(self.data['encryption']) / 40 ) * ( 1 + 0 / 100 )
        datacore = InputInvention.objects.filter(inventions=bp_invention)
        for core in datacore:
            #print(core.items.name, core.quantity, ">>>>", (core.quantity / chance))
            data[core.items.name] = ( core.quantity / chance ) / bp.quantity_produced
        return data


    def check_material_only(self, data):

        for key in data.keys():
            item = Item.objects.get(name=key)
            if item.group_belong.name == "Fuel Block":
                if self.data["fuel_block"] == False:
                    continue  
            if self.data["arborescence"] == '1':
                if item.group_belong.name in FROM_REACTION:
                    pass
                else:
                    try:
                        Blueprint.objects.get(items_produced__name=key)
                        return False
                    except ObjectDoesNotExist:
                        pass
            else:
                try:
                    Blueprint.objects.get(items_produced__name=key)
                    return False
                except ObjectDoesNotExist:
                    pass
        return True

    def craft_detail(self, data):

        detail = {}
        for key, value in data.items():
            item = Item.objects.get(name=key)
            if item.group_belong.name == "Fuel Block":
                if self.data["fuel_block"] == False:
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