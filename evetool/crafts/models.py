from django.db import models

class Category(models.Model):
    """categories model"""
    name = models.CharField(max_length=200, unique=True)
    categories_id = models.IntegerField(unique=True)


class Group(models.Model):
    """groups in a category"""
    name = models.CharField(max_length=200, unique=True)
    groups_id = models.IntegerField(unique=True)
    category_belong = models.ForeignKey(Category, on_delete=models.CASCADE)


class Item(models.Model):
    """items in a group"""
    name = models.CharField(max_length=200, unique=True)
    types_id = models.IntegerField(unique=True)
    group_belong = models.ForeignKey(Group, on_delete=models.CASCADE)
    week0_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    week1_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    month0_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    month1_value = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    week0_quantity = models.BigIntegerField(null=True)
    week1_quantity = models.BigIntegerField(null=True)
    month0_quantity = models.BigIntegerField(null=True)
    month1_quantity = models.BigIntegerField(null=True)

class Blueprint(models.Model):
    """blueprint model"""
    name = models.CharField(max_length=200, unique=True)
    types_id = models.IntegerField(unique=True)
    group_belong = models.ForeignKey(Group, on_delete=models.CASCADE)
    items_needed = models.ManyToManyField(Item, related_name="compo",through="InputProduction")
    items_produced = models.ForeignKey(Item, related_name="result", on_delete=models.CASCADE, null=True)
    quantity_produced = models.IntegerField(null=True)
    invention_data = models.ManyToManyField("self", through="Invention", symmetrical=False)
    tech_2 = models.BooleanField(default=False)
    reaction = models.BooleanField(default=False)
    time_prod = models.IntegerField(default=3600)


class Invention(models.Model):
    """data linked to invention"""
    input_blueprint = models.ForeignKey(Blueprint, related_name="input_bp", on_delete=models.CASCADE)
    output_blueprint = models.ForeignKey(Blueprint, related_name="output_bp", on_delete=models.CASCADE)
    items_needed = models.ManyToManyField(Item, through="InputInvention")
    time = models.IntegerField()
    run_per_success = models.IntegerField(default=1)
    succes_rate = models.DecimalField(max_digits=6, decimal_places=2)


class InputProduction(models.Model):
    """items needed for blueprint"""
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    blueprints = models.ForeignKey(Blueprint, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class InputInvention(models.Model):
    """items needed for invention"""
    items = models.ForeignKey(Item, on_delete=models.CASCADE)
    inventions = models.ForeignKey(Invention, on_delete=models.CASCADE)
    quantity = models.IntegerField()
