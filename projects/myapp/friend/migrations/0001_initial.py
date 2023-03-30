# Generated by Django 4.1.7 on 2023-03-21 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Friend",
            fields=[
                # 모델을 만들 때 기본키를 추가하지 않으면 id라는 열이 자동 생성(1~숫자)
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("friend_name", models.CharField(max_length=10)),
                ("friend_age", models.IntegerField()),
                ("friend_bigo", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
