# Generated by Django 4.1.7 on 2023-04-03 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0007_board_attached_file_board_orginal_file_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="board",
            old_name="orginal_file_name",
            new_name="original_file_name",
        ),
    ]