# Generated by Django 4.0.4 on 2023-05-12 06:06

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_product_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_information',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
