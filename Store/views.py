from django.shortcuts import render,HttpResponseRedirect
from Store.models import *
from Qshop.views import setPassword,loginValid_store

@loginValid_store
def index(request):
    return render(request,"store/base.html")

def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        store = Store.objects.filter(login_name = username).first()
        if store:
            form_password = setPassword(password)
            db_password = store.password
            if form_password == db_password:
                response = HttpResponseRedirect("/Store/index/")
                response.set_cookie("username",store.login_name)
                return response
    return render(request,"store/login.html")

def register(request):
    """
    注册店铺
    """
    if request.method == "POST" and request.POST:
        data = request.POST
        img = request.FILES.get("logo")
        store = Store()
        store.store_name = data.get("store_name")
        store.login_name = data.get("username")
        store.password = setPassword(data.get("password"))
        store.email = data.get("email")
        store.phone = data.get("phone")
        store.address = data.get("address")
        store.logo = img
        store.save()
        return HttpResponseRedirect("/Store/login/")
    return render(request,"store/register.html")

def logout(request):
    response = HttpResponseRedirect("/Store/login/")
    response.delete_cookie("username")
    return response

def addCommodity(request):
    types = Type.objects.all()
    if request.method == "POST":
        data = request.POST
        name = data.get("name")
        price = data.get("price")
        number = data.get("number")
        datas = data.get("data")
        safe = data.get("safe")
        address = data.get("address")
        types = data.get("types")
        picture = request.FILES.get("picture")
        content = data.get("content")

        c = Commodity()
        c.commodity_name = name
        c.commodity_id = "131221354"
        c.commodity_price = price
        c.commodity_number = number
        c.commodity_picture = picture
        c.commodity_data = datas
        c.commodity_safe_data = safe
        c.commodity_address = address
        c.commodity_content = content
        c.delete_flage = "false"
        c.type = Type.objects.get(id = int(types))  #添加外键
        store_login_name = request.COOKIES.get("username")  #通过cookie获取的店铺登录名称
        store = Store.objects.get(login_name=store_login_name)  #通过登录名称获取商店数据
        c.shop = store
        c.save()
        #添加多对的关系
        # store_login_name = request.COOKIES.get("username")  #通过cookie获取的店铺登录名称
        # store = Store.objects.get(login_name=store_login_name)  #通过登录名称获取商店数据

        return HttpResponseRedirect("/Store/listCom/up/1/")
    return render(request,"store/addCommodity.html",locals())
from django.core.paginator import Paginator

def listCommodity(request,type,page):
    page_int = int(page)
    if type == "down":
        commodity_list = Commodity.objects.filter(delete_flage="true").order_by("-commodity_data")
    else:
        commodity_list = Commodity.objects.filter(delete_flage="false").order_by("-commodity_data")
    paginator = Paginator(commodity_list,10)
    page = paginator.page(page_int)
    if page_int < 4:
        page_range = range(1,6)
    else:
        page_range = paginator.page_range[page_int-3:page_int+2]
    return render(request,"store/listCommodity.html",{"page_data":page,"page_range":page_range,"type":type})

def soldCommodity(request,type,id):
    referer = request.META.get("HTTP_REFERER")
    commodity = Commodity.objects.get(id = int(id))
    if type == "up":
        commodity.delete_flage = "false"
    else:
        commodity.delete_flage = "true"
    commodity.save()

    return HttpResponseRedirect(referer)

def addType(request):
    Types = Type.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        types = request.POST.get("types")
        picture = request.FILES.get("picture")

        t = Type()
        t.name = name
        t.parent = types
        t.picture = picture
        t.save()
    return render(request,"store/addType.html",locals())

# Create your views here.
from django.http import HttpResponse
import random
def addData(request):
    # types = ["海产","肉类","粮油","蛋奶","水果","海外"]
    # # for t in types:
    # #     ty = Type()
    # #     ty.name = t
    # #     ty.parent = 0
    # #     ty.save()
    commodity = ["牛肉","大虾","樱桃","鲜奶","大米","牛排"]
    country = "中国、蒙古、朝鲜、韩国、日本、菲律宾、越南、老挝、柬埔寨、缅甸、泰国、马来西亚、文莱、新加坡、印度尼西亚、东帝汶、尼泊尔、不丹、孟加拉国、印度、巴基斯坦、斯里兰卡、马尔代夫".split("、")
    for i in range(10000):
        com = Commodity()
        c = random.choice(country)
        com.commodity_name = c+random.choice(commodity)
        com.commodity_id = str(i).zfill(9)
        com.commodity_price = random.randint(100,1000)
        com.commodity_number = 1000
        com.commodity_data = "%s-%s-%s"%(random.randint(1000,3000),random.randint(1,12),random.randint(1,28))
        com.commodity_safe_data = 120
        com.commodity_address = c
        com.commodity_content = "嘎嘣脆，鸡肉味"

        com.delete_flage = "false"
        com.type = Type.objects.get(id = random.randint(1,6))
        com.save()
        com.shop.add(Store.objects.get(login_name="laobian"))
        com.save()
    return HttpResponse("保存成功")

def order_list(request):
    store=Store.objects.get(login_name=request.COOKIES.get("username"))
    order_list=store.orderresource_set.all()
    return render(request,"store/order_list.html",locals())