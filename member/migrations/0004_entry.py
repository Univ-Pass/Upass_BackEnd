# Generated by Django 3.2 on 2021-05-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_member_wallet_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.CharField(max_length=50, null=True)),
                ('building_num', models.CharField(max_length=30, null=True)),
                ('entry_did', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
