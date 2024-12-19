from ctypes import c_double
from itertools import product

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import AbstractUser
from django.db import models


class Sell(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField()
    date = models.DateField(auto_now=True)


class AdminSellList(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField()
    flyers = models.IntegerField(default=0)


class Evaluation(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    evaluation = models.PositiveIntegerField()
    text = models.CharField(max_length=1024)


class Product(models.Model):
    name = models.CharField(max_length=50)
    numm_evaluation = models.FloatField(default=0)
    count_evaluation = models.IntegerField(default=0)
    prise = models.FloatField()
    img_url = models.URLField()
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    count = models.IntegerField()
    cost_price = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            o = AdminSellList.objects.get(product=self)

        except:
            sell_list = AdminSellList(product=self, count=0)
            sell_list.save()


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    cart = models.ManyToManyField(Product)

    def __str__(self):
        return self.username


class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class CountProduct(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    count = models.ManyToManyField(CountProduct)
    prise = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        res = 0
        for i in self.count.all():
            res += i.product.prise * i.count
        self.prise = res
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        super().delete()


class Feedback(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    question = models.CharField(max_length=25)
    description = models.CharField(max_length=500)


class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='user',
                             related_name='from_user', db_index=True)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='recipient',
                                  related_name='to_user', db_index=True)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False,
                                     db_index=True)
    body = models.TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def save(self, *args, **kwargs):
        new = self.id
        self.body = self.body.strip()
        super(MessageModel, self).save(*args, **kwargs)

    class Meta:
        app_label = 'app'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
