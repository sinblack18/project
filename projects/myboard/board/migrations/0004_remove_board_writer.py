# Generated by Django 4.1.7 on 2023-03-28 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0003_rename_title_board_title1"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="board",
            name="writer",
        ),
    ]