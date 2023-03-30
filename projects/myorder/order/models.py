from django.db import models
from django.utils import timezone  # 시간정보에 관한 모듈

# Create your models here.


class Order(models.Model):

    order_date = models.DateTimeField(default=timezone.now)  # 주문 시간
    order_text = models.TextField(null=False, blank=False)  # 주문 내용
    price = models.IntegerField(default=0)  # 가격
    address = models.CharField(max_length=200)  # 주소
