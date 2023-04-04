from django.db import models
from django.utils import timezone  # 시간정보에 관한 모듈

# Create your models here.


class Itemlist(models.Model):
    # itemcode = models.CharField(max_length=20, primary_key=True)
    item_name = models.CharField(max_length=100)
    item_count = models.IntegerField(default=1)


class Orderlist(models.Model):
