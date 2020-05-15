from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from Store.models import *
from Buyer.models import *
from django.core.paginator import Paginator
from Qshop.views import setPassword,loginValid_buyer

@loginValid_buyer
def index(request):
    types = Type.objects.filter(parent=0)
    result = []
    print("python java123")
    for t in types:
        d = {}
        d["type"] = t#每一种类型
        d ["data"] = t.commodity_set.filter(delete_flage="false").order_by("commodity_data")[:4]
        #{"type":t,"data":[1,2,3,4]}
        result.append(d)
    return render(request,"buyer/index.html",locals())
@loginValid_buyer
def shop_list(request,type_id,page):
    page_int = int(page)
    commoditys = Type.objects.get(id = int(type_id)).commodity_set.filter(delete_flage="false")
    paginator = Paginator(commoditys, 20)
    page = paginator.page(page_int)
    if page_int < 4:
        page_range = range(1, 6)
    else:
        page_range = paginator.page_range[page_int - 3:page_int + 2]
    if page == 1:
        previous_page = 0
    else:
        previous_page = page_int-1
    next_page = page_int+1
    result = {"commoditys":page, #页面数据
              "page_range":page_range, #页码范围
              "type_id":type_id, #类型id
              "previous_page":previous_page, #上一页
              "next_page":next_page} #下一页
    return render(request,"buyer/list.html",result)
@loginValid_buyer
def detail(request,com_id):
    commodity = Commodity.objects.get(id = int(com_id))
    if request.method == "POST":
        number = request.POST.get("number")
        car = BuyCar()
        car.commodity_name = commodity.commodity_name #商品名称
        car.commodity_id = commodity.id  # 商品id
        car.commodity_price = commodity.commodity_price  # 商品价格
        car.commodity_picture = commodity.commodity_picture  # 商品图片

        car.commodity_number = number  # 购买商品数量

        car.shop_id = commodity.shop.id  # 商店的id
        car.user_id = request.COOKIES.get("user_id")  # 用户的id
        car.save()
        return HttpResponseRedirect("/Buyer/cart")
    return render(request,"buyer/detail.html",locals())
@loginValid_buyer
def cart(request):
    user_id = int(request.COOKIES.get("user_id"))
    shop_list = BuyCar.objects.filter(user_id=user_id)
    shops = []
    for shop in shop_list:
        shops.append({
            "id":shop.id,
            "commodity_name":shop.commodity_name,
            "commodity_id":shop.id,
            "commodity_price": shop.commodity_price,
            "commodity_number": shop.commodity_number,
            "commodity_picture": shop.commodity_picture,
            "total": shop.commodity_price*shop.commodity_number,
        })

    return render(request,"buyer/carts.html",locals())
def place_order(request):
    if request.method == "POST":
        add_list = Address.objects.all()
        data = request.POST
        car_shop_list = []
        for k,v in data.items():
            if v == "on":
                car_data = BuyCar.objects.get(id = int(k))
                car_shop_list.append(car_data)
        car_shop_list = enumerate(car_shop_list,1)
        return render(request,"buyer/place_order.html",locals())
    else:
        return HttpResponse("bad request method")

def register(request):
    if request.method == "POST":
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")

        user = BuyUser()
        user.login_name = username
        user.password = setPassword(password)
        user.save()
        return HttpResponseRedirect("/")
    return render(request,"buyer/register.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        user = BuyUser.objects.filter(login_name = username).first()
        if user:
            db_password = user.password
            form_password = setPassword(password)
            if db_password == form_password:
                response = HttpResponseRedirect("/")
                response.set_cookie("username",user.login_name)
                response.set_cookie("user_id",user.id)
                return response
    return render(request,"buyer/login.html")
@loginValid_buyer
def userCenter(request):
    return render(request,"buyer/user_center.html")

@loginValid_buyer
def userCenterOrder(request):
    return render(request,"buyer/user_center_order.html")
#
@loginValid_buyer
def userCenterSite(request):
    add_list = Address.objects.all()
    if request.method == "POST":
        recver = request.POST.get("recver")
        addr = request.POST.get("adress")
        phone = request.POST.get("phone")

        address = Address()
        address.address = addr
        address.recver = recver
        address.phone = phone
        address.buyer_id = BuyUser.objects.get(id = int(request.COOKIES.get("user_id")))
        address.save()
    return render(request,"buyer/user_center_site.html",locals())

from alipay import AliPay
import datetime
def Pay(request):
    if request.method=="GET" and request.GET:
        data=request.GET
        data_item=data.items()

        order=  Order()
        order.user_address=Address.objects.get(id=1)
        order.state=0
        order.date=datetime.datetime.now()
        order.user_id=BuyUser.objects.get(id=int(request.COOKIES.get("user_id")))
        order.save()
        order.order_number=str(order.id).zfill(10)
        order.save()
        money=0
        for k,v in data_item:
            if k.startswith("shop_"):
                car_id=int(v)
                data=BuyCar.objects.get(id=car_id)
                order_resource=OrderResource()
                order_resource.commodity_name=data.commodity_name
                order_resource.commodity_id = data.commodity_id
                order_resource.commodity_price = data.commodity_price
                order_resource.commodity_number = data.commodity_number
                order_resource.small_money = data.commodity_price*data.commodity_number
                order_resource.commodity_picture = data.commodity_picture
                order_resource.order_id=order
                order_resource.store_id=Store.objects.get(id=data.shop_id)
                order_resource.save()
                money +=order_resource.small_money
            order.money=money
            alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
                    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0YkPYl47TazlRtotjnhJCBsc2cVmadTGJwCXpRmbzRmUcEdZ20qQx0GwhrvZqgpoEmeO9gyG89Rdcu/6wLxYKdD5n2cAXHzQfAyajdHCfHmItVzqh2OTJViqhH5I/cWbqrhYnd7Y0ZqdADIps2upqyjbJvj2Pm+H0nJUxU9YN4c6cSvF08jCjFyva65u2+OGdK/K5zRCiNCSSEjMs+R9YaMqAfrBzbEU6lGgldDZ4Qov87UrfugmRImHsOtNeyq2eLBHilCUBQ2hIIRT+6s6kJxQF2N/8r6vlh02Fv8HHS477QTBpxkfeCM0No2HfYi/D2AVlDQxzyGTXgD9QrXUewIDAQAB
                -----END PUBLIC KEY-----'''

            app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
                    MIIEpAIBAAKCAQEA0YkPYl47TazlRtotjnhJCBsc2cVmadTGJwCXpRmbzRmUcEdZ20qQx0GwhrvZqgpoEmeO9gyG89Rdcu/6wLxYKdD5n2cAXHzQfAyajdHCfHmItVzqh2OTJViqhH5I/cWbqrhYnd7Y0ZqdADIps2upqyjbJvj2Pm+H0nJUxU9YN4c6cSvF08jCjFyva65u2+OGdK/K5zRCiNCSSEjMs+R9YaMqAfrBzbEU6lGgldDZ4Qov87UrfugmRImHsOtNeyq2eLBHilCUBQ2hIIRT+6s6kJxQF2N/8r6vlh02Fv8HHS477QTBpxkfeCM0No2HfYi/D2AVlDQxzyGTXgD9QrXUewIDAQABAoIBAQCZ75qIxvfEefe7FMCRQVdOCDUq2/YAXBvzPWErHuQySs+dqR2fmGlCqcTZRxqC7MBGfSQvKUbfzS2WKi3K+NPAbNFmxRIj4GJ+L/g/plG+hr7jls6KBqJstnYXfnt7THivdF1OJhCd9HvRUAkI0ljE8PAH8rFdbyyWc/5JMqB5sZ+e5IisDHL7s0oWwYVllox2XZ/211N6+96K9Emd7ESd7NTH8KlJ4cZEecV8J+91P/HwcSNxAuKXKvPX3nbXbo5HRMJYof4wolEWKJeOBc17jy3jEb4XHyiFeYF2Y6n480yvt6GWPh/BSXNuW4c41nGcpVPHDsh9Nqn/5RxylWf5AoGBAPIfbl42rsBcNTCZEJufSJ7n9AE0qMNjA3irFNVO4jD1xKTW0Qb2E8cBouxlZgZAEk4rkFPO1QYw4kr0wofnmR7FOx6+829aHv1IQDtvDkmra70klfC/4cTUx/sfwckqKDgPYzIbSZ/MDl+On7CesLJtSodSzL7ZRBwl+cwF2Ec9AoGBAN2LfM4N3sl92dM29kHr0s1oAL4xthRHVCEJoRG32Wb35uggHKCe+LrvBoU9bmLF/nwXV0k3dgTsHOB9jf/TRSq2ipVzl+9OylN4QJ682k1o9sfXVOzgDG/4dGN6GLIr401QvPwFGshoQYhaHT+WfGm1JsZ963aTdi5NnV7ezAYXAoGASTlQO5X2C57XRzdDWo01fTlRBfxS/aQ4LIow5sHQjlYFfoSo+p35JTpNd4jC7ij6YEG0iGQI8LJf/aNAIbHdEP08//Nn08lBjgAHzPGtNIJvNuiVoBWnxctEH6JfDON+/lVI/qJaBcXEowmTKesULSH4ZCyaVy2F961UemtaGVECgYEAuIyWtYsmWBCHIIQ7VSSeIM+PNuBwPapBcZf03a6Z4kWFyz3cuwxSRF4Sv3EyAAPQ/wvugSY7INSTJYpRfJdAmdkfzmlRWl72+dtFcTX+X9edI1HEA+KLWcbNJYSzB9C5c1FbbFDQQ7tdQ7lVff/cua3WlCiWudsS6nVrL3lG2ZcCgYANwqhHVWKHrOJO6xr8OygSMuXDNHPutm+DJIkbjHjKi0fShW3hat4YqTG0x5Rotu+R36p1reiNSmyIvOgrXtV4Ab/s/2X2FhFKoER0j5Ql/jEmr1IjKsZqPIxFxPSrt2y0BmPlqEOlnAn10WZSRP7UTCZAEVOp5jEfuBRHUC4OQw==
                -----END RSA PRIVATE KEY-----'''

            # 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
            # 在windows下，默认生成的txt文件，会有两个问题
            # 1、格式不标准
            # 2、编码不正确 windows 默认编码是gbk

            # 实例化应用
            alipay = AliPay(
                appid="2016093000628363",  # 支付宝app的id
                app_notify_url=None,  # 回调视图
                app_private_key_string=app_private_key_string,  # 私钥字符
                alipay_public_key_string=alipay_public_key_string,  # 公钥字符
                sign_type="RSA2",  # 加密方法
            )
            # 发起支付
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order.order_number,  # 订单号
                total_amount=str(order.money),  # 将Decimal类型转换为字符串交给支付宝
                subject="商贸商城",
                return_url=None,
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            # 让用户进行支付的支付宝页面网址
            # print("https://openapi.alipaydev.com/gateway.do?" + order_string)
            return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
# Create your views here.








