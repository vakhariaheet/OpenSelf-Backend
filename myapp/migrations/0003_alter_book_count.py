# Generated by Django 5.0.6 on 2024-07-14 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_book_arrival_date_remove_book_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='count',
            field=models.IntegerField(),
        ),
    ]