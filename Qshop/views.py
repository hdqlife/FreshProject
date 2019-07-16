import hashlib
from django.shortcuts import HttpResponseRedirect

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

def loginValid_store(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Store/login/")
    return inner

def loginValid_buyer(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get("username")
        if username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/Buyer/login/")
    return inner

from alipay import AliPay
def alipay(request):

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
        out_trade_no="34835426",  # 订单号
        total_amount=str(0.01),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url=None,
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 让用户进行支付的支付宝页面网址
    # print("https://openapi.alipaydev.com/gateway.do?" + order_string)
    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)