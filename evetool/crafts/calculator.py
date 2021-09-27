from crafts.models import Item
from config import MARKET_FEE, COST_INDEX


class Calculator():

    def __init__(self, item_bp, runs):
        self.item = item_bp.items_produced
        self.bp = item_bp
        self.runs = runs
        self.stats = {}

    def give_benef(self, compo):
        """calcul and return item benef + variation"""
        self.calcul_input_value(compo)
        self.calcul_benef()
        self.calcul_progress()
        return self.stats

    def give_info(self, compo):
        """calcul and prepare item's data"""
        self.calcul_input_value(compo)
        self.calcul_benef()
        self.calcul_info()
        self.more_info(compo)
        return self.stats

    def calcul_input_value(self, compo):
        """calcul all components value"""
        self.week0 = 0
        self.week1 = 0
        self.month0 = 0
        self.month1 = 0
        for key, value in compo.items():
            item = Item.objects.get(name=key)
            try:
                self.week0 += float(item.week0_value) * value
            except TypeError:
                # MARKET DATA ERROR USUALLY ITEM NOT IN GAME MARKET
                self.week0 = 0
            try:
                self.week1 += float(item.week1_value) * value
            except TypeError:
                # MARKET DATA ERROR USUALLY ITEM NOT IN GAME MARKET
                self.week1 = 0
            try:
                self.month0 += float(item.month0_value) * value
            except TypeError:
                # MARKET DATA ERROR USUALLY ITEM NOT IN GAME MARKET
                self.month0 = 0
            try:
                self.month1 += float(item.month1_value) * value
            except TypeError:
                # MARKET DATA ERROR USUALLY ITEM NOT IN GAME MARKET
                self.month1 = 0

    def calcul_benef(self):
        """calcul item benef from input"""
        if self.week0 == 0:
            self.stats["DAY_PROFIT_WEEK"] = "ERROR WITH MARKET DATA"
        else:
            try:
                week0_benef = (float(self.item.week0_value)
                               * MARKET_FEE - self.week0 * COST_INDEX)
                self.stats["DAY_PROFIT_WEEK"] = (week0_benef
                                                 * self.bp.quantity_produced) * self.runs
            except TypeError:
                self.stats["DAY_PROFIT_WEEK"] = "ERROR WITH MARKET DATA"
        if self.week1 == 0:
            self.day_profit_week1 = "ERROR WITH MARKET DATA"
        else:
            try:
                week1_benef = (float(self.item.week1_value)
                               * MARKET_FEE - self.week1 * COST_INDEX)
                self.day_profit_week1 = (week1_benef
                                         * self.bp.quantity_produced) * self.runs
            except TypeError:
                self.day_profit_week1 = "ERROR WITH MARKET DATA"
        if self.month0 == 0:
            self.stats["DAY_PROFIT_MONTH"] = "ERROR WITH MARKET DATA"
        else:
            try:
                month0_benef = (float(self.item.month0_value) * MARKET_FEE
                                - self.month0 * COST_INDEX)
                self.stats["DAY_PROFIT_MONTH"] = (month0_benef
                                                  * self.bp.quantity_produced) * self.runs
            except TypeError:
                self.stats["DAY_PROFIT_MONTH"] = "ERROR WITH MARKET DATA"
        if self.month1 == 0:
            self.day_profit_month1 = "ERROR WITH MARKET DATA"
        else:
            try:
                month1_benef = (float(self.item.month1_value) * MARKET_FEE
                                - self.month1 * COST_INDEX)
                self.day_profit_month1 = (month1_benef
                                          * self.bp.quantity_produced) * self.runs
            except TypeError:
                self.day_profit_month1 = "ERROR WITH MARKET DATA"

    def calcul_progress(self):
        """calcul evolution of price"""
        if self.item.month0_quantity is None:
            self.stats["volume"] = 0
        else:
            self.stats["volume"] = float(self.item.month0_quantity)
        self.stats["runs_day"] = self.runs
        if self.stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA" \
                or self.day_profit_week1 == "ERROR WITH MARKET DATA":
            self.stats['day_profit_week_progress'] = 0
        else:
            self.stats['day_profit_week_progress'] = ((self.stats["DAY_PROFIT_WEEK"]
                                                      * 100) / self.day_profit_week1) - 100
        if self.stats["DAY_PROFIT_MONTH"] == "ERROR WITH MARKET DATA" \
                or self.day_profit_month1 == "ERROR WITH MARKET DATA":
            self.stats["day_profit_month_progress"] = 0
        else:
            self.stats["day_profit_month_progress"] = ((self.stats["DAY_PROFIT_MONTH"] * 100)
                                                       / self.day_profit_month1) - 100

    def calcul_info(self):
        """calcul_progress() with more detail """
        if self.stats["DAY_PROFIT_WEEK"] == "ERROR WITH MARKET DATA" \
                or self.day_profit_week1 == "ERROR WITH MARKET DATA":
            self.stats["DAY_PROFIT_WEEK_PROGRESS"] = 0
            self.stats["compo_progress_week"] = 0
            self.stats["product_progress_week"] = 0
            self.stats["volume_progress_week"] = 0
        else:
            self.stats["DAY_PROFIT_WEEK_PROGRESS"] = ((self.stats["DAY_PROFIT_WEEK"] * 100)
                                                      / self.day_profit_week1) - 100
            self.stats["compo_progress_week"] = self.week0 * 100 / self.week1 - 100
            self.stats["product_progress_week"] = (float(self.item.week0_value) * 100
                                                   / float(self.item.week1_value) - 100)
            self.stats["volume_progress_week"] = (float(self.item.week0_quantity) * 100
                                                  / float(self.item.week1_quantity) - 100)
        if self.stats["DAY_PROFIT_MONTH"] == "ERROR WITH MARKET DATA" \
                or self.day_profit_month1 == "ERROR WITH MARKET DATA":
            self.stats["DAY_PROFIT_MONTH_PROGRESS"] = 0
            self.stats["compo_progress_month"] = 0
            self.stats["product_progress_month"] = 0
            self.stats["volume_progress_month"] = 0
        else:
            self.stats["DAY_PROFIT_MONTH_PROGRESS"] = ((self.stats["DAY_PROFIT_MONTH"] * 100)
                                                       / self.day_profit_month1) - 100
            self.stats["compo_progress_month"] = self.month0 * 100 / self.month1 - 100
            self.stats["product_progress_month"] = (float(self.item.month0_value) * 100
                                                    / float(self.item.month1_value) - 100)
            self.stats["volume_progress_month"] = (float(self.item.month0_quantity) * 100
                                                   / float(self.item.month1_quantity) - 100)

    def more_info(self, compo):
        """add more data related to item"""
        self.stats["RUNS_DAY"] = self.runs * self.bp.quantity_produced
        self.stats["compo_value_week"] = self.week0
        self.stats["compo_value_month"] = self.month0
        self.stats["list_components"] = compo
        self.stats["item_selected"] = self.item.name

        if self.item.week0_value is None:
            self.stats["product_value_week"] = None
        else:
            self.stats["product_value_week"] = float(self.item.week0_value)
        if self.item.month0_value is None:
            self.stats["product_value_month"] = None
        else:
            self.stats["product_value_month"] = float(self.item.month0_value)
        if self.item.week0_quantity is None:
            self.stats["VOLUME"] = None
        else:
            self.stats["VOLUME"] = float(self.item.week0_quantity)
        if self.item.month0_quantity is None:
            self.stats["product_volume_month"] = None
        else:
            self.stats["product_volume_month"] = float(self.item.month0_quantity)
