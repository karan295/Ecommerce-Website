# Generated by Django 2.2.5 on 2021-02-02 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashionable Jewel'), ('Antique', 'Antique Jewel'), ('design', 'Designable Jewel'), ('daily', 'Daily Useable Jewel')], max_length=2),
        ),
    ]