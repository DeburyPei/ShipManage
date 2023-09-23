from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Func, DateField
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.parsers import JSONParser
from django.http import JsonResponse,HttpResponse
from .models import *
from .serializers import *
from rest_framework.documentation import include_docs_urls
import requests,json,re
from lxml import etree






# ---------------------------------------user ---------------------------------------
@csrf_exempt
def userLogin(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = UserInfo.objects.filter(name=data["params"]["name"],password=data["params"]["password"],status=1)
        if users.exists():
            serializer = UserInfoSerializer(users, many=True)
            return JsonResponse({"code": "ok",'user':serializer.data}, status=200)
        else:
            return JsonResponse({"code": "error","messgae":"请检查账号或者密码"}, status=400)
    return JsonResponse({"code": "error"}, status=400)
@csrf_exempt
def adminLogin(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = Admin.objects.filter(name=data["params"]["name"],password=data["params"]["password"])
        if users.exists():

            return JsonResponse({"code": "ok"}, status=200)
        else:
            return JsonResponse({"code": "error","messgae":"请检查账号或者密码"}, status=400)
    return JsonResponse({"code": "error"}, status=400)
@csrf_exempt
def userRegister(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        b = UserInfo(name=data['params']['name'], password=data['params']['password'], phone=data['params']['phone'])
        b.save()
        
            
        return JsonResponse({"code": "ok","messgae":"注册成功"}, status=200)

    return JsonResponse({"code": "error","messgae":"注册失败"}, status=400)
@csrf_exempt
def userChangePwd(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data["params"])
        users = UserInfo.objects.get(id=data["params"]["user_id"],password=data["params"]["oldPass"])
        if users != None:
            users.password = data["params"]["checkPass"]
            users.save()
            return JsonResponse({"code": "ok"}, status=200)
        else:
            return JsonResponse({"code": "error","messgae":"旧密码不正确"}, status=400)
    return JsonResponse({"code": "error"}, status=400)

@csrf_exempt
def createOrderInfo(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":

        posts = Port.objects.all()
        serializer_posts = PortSerializer(posts, many=True)
        cargos = Cargo.objects.filter(user_id=request.GET.get('user_id'),status="False")
        serializer_cargos = CargoSerializer(cargos, many=True)
        ships = ShipInfo.objects.all()
        serializer_ships = ShipInfoSerializer(ships, many=True)
        return JsonResponse({"port":serializer_posts.data,"cargos":serializer_cargos.data,"ships":serializer_ships.data}, safe=False,status=200)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":

        return JsonResponse({"code":"error"}, status=400)


@csrf_exempt
def createOrder(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        port1 = Port.objects.filter(id=data['params']['startPortId']).values('nowCity')
        port2 = Port.objects.filter(id=data['params']['endPortId']).values('nowCity')
        shipSpeedPrice = ShipInfo.objects.filter(id=data['params']['shipId']).values('price')
        distance = getDistance(port1[0]['nowCity'],port2[0]['nowCity'])
        print(shipSpeedPrice[0]["price"],distance)
        price = int(shipSpeedPrice[0]["price"])*int(distance)
        print(price)
        b = Order(ship_id=data['params']['shipId'], cargo_id=data['params']['cargoId'],
                  start_port_id=data['params']['startPortId'],
                  end_port_id=data['params']['endPortId'],
                  Remark=data['params']['reMark'],
                  price=price,
                  distance=distance,
                  user_id=  data['params']['user_id'],
                  orderNum=data['params']['orderNum']
                  )
        b.save()
        return JsonResponse({"code": "ok","price":price,"distance":distance}, status=200)


    return JsonResponse({"code": "error", "messgae": "提交失败"}, status=400)

@csrf_exempt
def getOrder(request):
    if request.method == "GET":

        users = Order.objects.filter(user_id=request.GET.get("id"))

        if users.exists():
            serializer = OrderSerializer(users, many=True)
            return JsonResponse({"code": "ok",'orders':serializer.data}, status=200)
        else:
            return JsonResponse({"code": "error","messgae":"请检查账号或者密码"}, status=400)
    return JsonResponse({"code": "error"}, status=400)
@csrf_exempt
def getOrderById(request):
    if request.method == "GET":
        users = Order.objects.filter(orderNum=request.GET.get("id"))
        if users.exists():
            serializer = OrderSerializer(users, many=True)
            return JsonResponse({"code": "ok",'orders':serializer.data}, status=200)
        else:
            return JsonResponse({"code": "error","messgae":"请检查账号或者密码"}, status=400)
    return JsonResponse({"code": "error"}, status=400)


def getDistance(c1,c2):
    # print("c1",c1)
    def getCityName(a):
        city = a[a.find("省"):a.find("市")].replace("省", "")
        # print(city)
        response = requests.post("https://zhongwenzhuanpinyin.bmcx.com/web_system/bmcx_com_www/system/file/zhongwenzhuanpinyin/data_v2/?ajaxtimestamp=1683036697900",data={
            "zwzyp_zhongwen": city,
            "zwzyp_shengdiao": 0,
            "zwzyp_duozhongduyin": 0,
            "zwzyp_shouzimudaxie": 0,
        }).text
        # print(response)
        city1 = ""
        for i in json.loads(response):

            city1+=i["拼音"][0]
        return city1

    city1 = getCityName(c1)
    city2 = getCityName(c2)
    html = etree.HTML(requests.get(f"https://www.thedistancenow.com/zh/{city1}_china/{city2}_china").text)
    distance = html.xpath("/html/body/div[5]/h3[1]")[0].text.replace(" 公里","")
    print(distance)
    return distance
@csrf_exempt
def payorder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Order.objects.get(orderNum=data['params']['orderNum'])
        b.status = 2  #待发货


        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def qianshouOrder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Order.objects.get(orderNum=data['params']['orderNum'])
        b.status = 4  #签收 -》 待评价


        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def commentOrder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Order.objects.get(orderNum=data['params']['orderNum'])
        b.status = 5  #待评价 -》 已完成
        b.is_commented = True
        b.comment = data['params']['comment']


        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def userdeleteOrder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Order.objects.get(orderNum=data['params']['orderNum'])
        b.status = 6  #取消



        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def getCargos(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = Cargo.objects.filter(user_id=request.GET.get("user_id"))
        # print(posts.all())
        # posts["type"] =ShipType.objects.get(id=posts["type_id"])
        serializer = CargoSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":

        return JsonResponse({"code":"error"}, status=400)


@csrf_exempt
def user_edit_cargos(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Cargo.objects.get(id=data['params']['id'])


        b.name = data['params']['form']['cargo_name']
        b.type = data['params']['form']['cargo_type']
        b.weight = data['params']['form']['weight']




        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
def getPieSeris(allTypes):
    x = [ y['type'] for y in allTypes]

    dict = {}
    for key in x:
        dict[key] = dict.get(key, 0) + 1
    r = []
    for key,value in dict.items():
        r.append({"value":value,"name":key})
    return r
@csrf_exempt
def getMain(request):
    if request.method == "GET":

        orders = Order.objects.filter(user_id=request.GET.get("user_id"))
        ord_num = orders.count()
        ord_ok_num =  Order.objects.filter(user_id=request.GET.get("user_id"),status=5).count()

        cargo_num = Cargo.objects.filter(user_id=request.GET.get("user_id")).count()
        cargo_ok_num = Cargo.objects.filter(user_id=request.GET.get("user_id"),status=1).count()
        allTypes = Cargo.objects.filter(user_id=request.GET.get("user_id")).values('type')
        seriesData = getPieSeris(allTypes)

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse({'orders':serializer.data,"ord_num":ord_num,"ord_ok_num":ord_ok_num,"seriesData":seriesData,"cargo_num":cargo_num,"cargo_ok_num":cargo_ok_num}, status=200)

    return JsonResponse({"code": "error"}, status=400)
# ---------------------------------------order ---------------------------------------
@csrf_exempt
def orders_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据

    return JsonResponse({"code": "error"}, status=400)
@csrf_exempt
def deleteOrder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params']['id'])
        b = Order.objects.get(id=data['params']['id'])
        b.delete()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def searchOrder(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)

        users = UserInfo.objects.filter(name=data["params"]["name"]).values('id')
        print(users[0]['id'])
        orders = Order.objects.filter(user_id=users[0]['id'])
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"code":"error"}, status=500)



@csrf_exempt
def getTask(request):
    print(request.method)
    if request.method == "GET":

        orders = Order.objects.filter(status=2)
        serializer = OrderSerializer(orders, many=True)

        # b = Order.objects.get(orderNum=data['params']['orderNum'])
        # b.status = 2  #待发货
        # b.save()
        return JsonResponse(serializer.data, safe=False)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def getTaskDesc(request):
    print(request.method)
    if request.method == "GET":
        users = Order.objects.filter(orderNum=request.GET.get("id"))
        if users.exists():
            serializer = OrderSerializer(users, many=True)
            return JsonResponse({"code": "ok", 'orders': serializer.data}, status=200)
        else:
            return JsonResponse({"code": "error", "messgae": "请检查账号或者密码"}, status=400)
    return JsonResponse({"code": "error"}, status=400)

@csrf_exempt
def fahuo(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Order.objects.get(orderNum=data['params']['orderNum'])
        b.status = 3  #已发货
        b.kuaidiNum = data['params']['kuaidiId']
        b.save()
        c = Cargo.objects.get(id=b.cargo_id)
        c.status = 1  #货物状态 已完成
        c.save()


        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
# ---------------------------------------account ---------------------------------------
@csrf_exempt
def post_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = UserInfo.objects.all()
        serializer = UserInfoSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":
         # 将 request 中的参数取出来进行序列化
        data = JSONParser().parse(request)
        serializer = UserInfoSerializer(data=data)
         # 判断是否有效的数据
        if serializer.is_valid():
            # 有效数据保存，返回 201 CREATED
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # 无效则返回 400 BAD_REQUEST
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def addUser(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params']['name'])
        b = UserInfo(name=data['params']['name'], password=data['params']['password'],phone=data['params']['phone'])
        b.save()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)



@csrf_exempt
def deleteUser(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params']['id'])
        b = UserInfo.objects.get(id=data['params']['id'])
        b.delete()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def switchUser(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params']['id'])
        b = UserInfo.objects.get(id=data['params']['id'])

        b.status = not b.status
        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def editUser(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = UserInfo.objects.get(id=data['params']['id'])

        b.name = data['params']['form']['name']
        b.password = data['params']['form']['password']
        b.phone = data['params']['form']['phone']

        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def searchUser(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = UserInfo.objects.filter(name=data["params"]["name"])
        serializer = UserInfoSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"code":"error"}, status=500)

# ---------------------------------------Port---------------------------------------
@csrf_exempt
def ports_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = Port.objects.all()
        serializer = PortSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":

        return JsonResponse({"code":"error"}, status=400)

@csrf_exempt
def addPort(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])
        b = Port(name=data['params']['port_name'], nowCity=data['params']['now_city'])
        b.save()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def deletePort(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params']['id'])
        b = Port.objects.get(id=data['params']['id'])
        b.delete()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def editPort(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Port.objects.get(id=data['params']['id'])

        b.name = data['params']['form']['port_name']
        b.nowCity = data['params']['form']['now_city']


        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def searchPort(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = Port.objects.filter(name=data["params"]["name"])
        serializer = PortSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"code":"error"}, status=500)
# ---------------------------------------ship ---------------------------------------


@csrf_exempt
def ships_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = ShipInfo.objects.all()
        print(posts.query)

        # posts["type"] =ShipType.objects.get(id=posts["type_id"])
        serializer = ShipInfoSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":

        return JsonResponse({"code":"error"}, status=400)
@csrf_exempt
def addShip(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])
        b = ShipInfo(name=data['params']['ship_name'],
                     type_id=data['params']['type_id'],
                     port_id=data['params']['port_id'],
                     capacity=data['params']['capacity'],
                     price=data['params']['price'],
                     speed=data['params']['speed'])

        b.save()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def editShip(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = ShipInfo.objects.get(id=data['params']['id'])


        b.name = data['params']['form']['ship_name']
        b.type_id = data['params']['form']['type_id']
        b.port_id = data['params']['form']['port_id']
        b.capacity = data['params']['form']['capacity']
        b.price = data['params']['form']['price']
        b.speed = data['params']['form']['speed']




        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def searchShip(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = ShipInfo.objects.filter(name=data["params"]["name"])
        serializer = ShipInfoSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"code":"error"}, status=500)
# ---------------------------------------cargos ---------------------------------------
@csrf_exempt
def cargos_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = Cargo.objects.all()

        # posts["type"] =ShipType.objects.get(id=posts["type_id"])
        serializer = CargoSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":

        return JsonResponse({"code":"error"}, status=400)
@csrf_exempt
def addCargo(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)

        b = Cargo(name=data['params']['cargo_name'], type=data['params']['cargo_type']
                  ,weight=data['params']['weight'],user_id=data['params']['user_id'])
        b.save()

        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)
@csrf_exempt
def searchCargo(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        users = Cargo.objects.filter(name=data["params"]["name"])
        serializer = CargoSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse({"code":"error"}, status=500)

@csrf_exempt
def deleteCargo(request):
        print(request.method)
        if request.method == "POST":
            data = JSONParser().parse(request)
            print(data['params']['id'])
            b = Cargo.objects.get(id=data['params']['id'])
            b.delete()

            return JsonResponse({"code": "OK"}, status=200)
        return JsonResponse({"code": "error"}, status=500)


@csrf_exempt
def editCargo(request):
    print(request.method)
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data['params'])

        b = Cargo.objects.get(id=data['params']['id'])


        b.name = data['params']['form']['cargo_name']
        b.type = data['params']['form']['cargo_type']
        b.weight = data['params']['form']['weight']
        b.user_id = data['params']['form']['user_id']



        b.save()
        return JsonResponse({"code": "OK"}, status=200)
    return JsonResponse({"code":"error"}, status=500)

import jieba,os
#加载停用词表
def cipin_exec(txt):
    # print("txt",txt)
    words  = jieba.lcut(txt)

    GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'CS.txt')
    stopwords = [line.strip() for line in open(GDRAT_abs_path, encoding="utf-8").readlines()]


    counts = {}
    for word in words:
        #不在停用词表中
        if word not in stopwords:
            #不统计字数为一的词
            if len(word) == 1:
                continue
            else:
                counts[word] = counts.get(word,0) + 1
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    return_items = []
    for i in range(30):
        word, count = items[i]
        return_items.append({"name":word,"value":count})
    # print(return_items[:15])
    return return_items[:15]
def getLast7Day():
    import datetime

    # 获取当前日期
    today = datetime.date.today()

    # 定义一个列表，用于保存过去7天的日期
    last_7_days = []

    # 循环7次，分别获取过去7天的日期
    for i in range(7):
        # 使用 timedelta 计算过去的日期
        day = today - datetime.timedelta(days=i)

        # 将日期按照指定格式保存到列表中
        formatted_date = day.strftime("%Y-%m-%d")
        last_7_days.append(formatted_date)
    return last_7_days
@csrf_exempt
def adminGetAll(request):
    if request.method == "GET":
        orders = Order.objects.all()
        ord_num = Order.objects.all().count()
        user_num = UserInfo.objects.all().count()
        ord_ok_num =  Order.objects.filter(status=5).count()
        ord_not_ok_num =  Order.objects.filter(status=2).count()
        cargo_num = Cargo.objects.all().count()
        cargo_ok_num = Cargo.objects.filter(status=1).count()

        port_num = Port.objects.all().count()
        ship_num = ShipInfo.objects.all().count()

        from datetime import datetime, timedelta
        # 获取当前日期
        today = datetime.now()

        # 计算过去7天的日期范围
        start_date = today - timedelta(days=6)
        end_date = today + timedelta(days=1)

        # 查询过去7天每天的订单数量
        result = Order.objects.filter(create_time__range=[start_date.date(), end_date.date()]).values("create_time").annotate(count=Count("id"))[:7]
        # result = Order.objects.annotate(created_time=TruncDate('create_time')).values("created_time").annotate(total=Count('id'))


        formatted_result = [{'date': r['create_time'].strftime('%Y-%m-%d'), 'count': r['count']} for r in result]
        # counts_data = {item['date']: item['count'] for item in formatted_result}
        # print(counts_data)
        counts = {}
        for item in formatted_result:
            date = str(item['date'])
            count = item['count']
            if date in counts:
                counts[date] += count
            else:
                counts[date] = count

        order_7_shuju = []
        for a in getLast7Day():
            try:
                order_7_shuju.append(counts[a])
            except:
                order_7_shuju.append(0)
       
        ciyunData = cipin_exec("".join([ mark["Remark"] for mark in orders.values("Remark")]))

        sum_shouru = sum([x['price'] for x in orders.filter(status=5).values('price')])
        _com = [x['comment'] for x in orders.filter(is_commented=1).values('comment')]
        avg_comment = round(sum(_com)/len(_com),2)

        allTypes = Cargo.objects.all().values('type')
        seriesData = getPieSeris(allTypes)

        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(
            {'user_num':user_num,
             'ord_not_ok_num':ord_not_ok_num,
             'port_num':port_num,
             'ship_num':ship_num,
             'sum_shouru':sum_shouru,
             'avg_comment':avg_comment,
             'orders':serializer.data,
             "ord_num":ord_num,
             "ord_ok_num":ord_ok_num,
             "seriesData":seriesData,
             "cargo_num":cargo_num,
             "cargo_ok_num":cargo_ok_num,
             "ciyunData":ciyunData,
             "counts":order_7_shuju[::-1]
             }, status=200)

    return JsonResponse({"code": "error"}, status=400)