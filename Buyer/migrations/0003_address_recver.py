# Generated by Django 2.2.1 on 2019-05-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0002_buycar_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='recver',
            field=models.CharField(default='冯程程', max_length=32),
            preserve_default=False,
        ),
    ]