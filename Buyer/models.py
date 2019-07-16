from django.db import models
from Store.models import Store

class BuyUser(models.Model):
    login_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    username = models.CharField(max_length=32,blank=True,null=True)
    #blank = True django默认值为空,可以在数据库当中不填写数据
    #null = True django默认字段为null,在数据库当中写入null
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=32,blank=True,null=True)
    photo = models.ImageField(upload_to="buyer/images",blank=True,null=True)

    #user = BuyUser.objects.get(id=1).address_set.all()
    #
class BuyCar(models.Model):
    commodity_name = models.CharField(max_length=32) #商品名称
    commodity_id = models.IntegerField() #商品id
    commodity_price = models.FloatField() #商品价格
    commodity_number = models.IntegerField() #购买商品数量
    commodity_picture = models.ImageField(upload_to="buyer/images") #商品图片
    user_id = models.IntegerField() #用户的id
    shop_id = models.IntegerField() #商店的id

class Address(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=32)
    recver = models.CharField(max_length=32)
    buyer_id = models.ForeignKey(to=BuyUser,on_delete=True)
#Address.objects.get(id = 1).buyer_id.address

class Order(models.Model):
    """
    订单状态
        待支付    0
        支付      1
        已发货    2
        确认收货  3
    """
    order_number = models.CharField(max_length = 32,blank=True,null=True)#订单编号
    user_address = models.ForeignKey(to=Address,on_delete=True) #地址
    money = models.FloatField(blank=True,null=True) #金额
    state = models.IntegerField() #订单状态
    date = models.DateTimeField(auto_now = True)
    user_id = models.ForeignKey(to=BuyUser,on_delete=True)

class OrderResource(models.Model):
    commodity_name = models.CharField(max_length=32)  # 商品名称
    commodity_id = models.IntegerField()  # 商品id
    commodity_price = models.FloatField()  # 商品价格
    commodity_number = models.IntegerField()  # 购买商品数量
    commodity_picture = models.ImageField(upload_to="buyer/images")  # 商品图片
    small_money = models.FloatField() #订单小计  价格*数量
    order_id = models.ForeignKey(to=Order,on_delete=True) #订单id
    store_id = models.ForeignKey(to=Store,on_delete=True) #店铺id

class ValidCode(models.Model):
    code = models.CharField(max_length=6)
    loginNmae = models.CharField(max_length=32)
    time = models.FloatField()
    flag = models.CharField(max_length=4) #0 没有校验过，1 校验过

# Create your models here.
