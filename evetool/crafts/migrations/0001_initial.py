# Generated by Django 3.2 on 2021-04-27 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blueprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('types_id', models.IntegerField(unique=True)),
                ('quantity_produced', models.IntegerField()),
                ('tech_2', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('categories_id', models.IntegerField(unique=True)),
                ('groups_list', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('groups_id', models.IntegerField(unique=True)),
                ('types_list', models.CharField(max_length=200)),
                ('category_belong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.category')),
            ],
        ),
        migrations.CreateModel(
            name='InputInvention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('types_id', models.IntegerField(unique=True)),
                ('month_value', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('week_value', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('month_quantity', models.IntegerField(null=True)),
                ('week_quantity', models.IntegerField(null=True)),
                ('group_belong', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.group')),
            ],
        ),
        migrations.CreateModel(
            name='Invention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
                ('succes_rate', models.DecimalField(decimal_places=2, max_digits=6)),
                ('input_blueprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_bp', to='crafts.blueprint')),
                ('items_needed', models.ManyToManyField(through='crafts.InputInvention', to='crafts.Item')),
                ('output_blueprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='output_bp', to='crafts.blueprint')),
            ],
        ),
        migrations.CreateModel(
            name='InputProduction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('blueprints', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.blueprint')),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.item')),
            ],
        ),
        migrations.AddField(
            model_name='inputinvention',
            name='inventions',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.invention'),
        ),
        migrations.AddField(
            model_name='inputinvention',
            name='items',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.item'),
        ),
        migrations.AddField(
            model_name='blueprint',
            name='group_belong',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crafts.group'),
        ),
        migrations.AddField(
            model_name='blueprint',
            name='invention_data',
            field=models.ManyToManyField(through='crafts.Invention', to='crafts.Blueprint'),
        ),
        migrations.AddField(
            model_name='blueprint',
            name='items_needed',
            field=models.ManyToManyField(related_name='compo', through='crafts.InputProduction', to='crafts.Item'),
        ),
        migrations.AddField(
            model_name='blueprint',
            name='items_produced',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result', to='crafts.item'),
        ),
    ]
