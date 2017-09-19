from django.db import models

# Create your models here.

from django.db import models

class CartInfo(models.Model):
    user=models.ForeignKey('tt_user.UserInfo')
    goods=models.ForeignKey('tt_goods.GoodsInfo')
    count=models.IntegerField()

    def add(self,quality):
        self.count +=quality
        self.save()
        return self.count

    def minus(self,quality):
        self.count -=quality
        self.save()
        return self.count

    def sumprice(self):
        return self.goods.gprice*self.count
