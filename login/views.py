from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import MyUser,CarDetails,startPooling,userPooling
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login, logout
import json
# Create your views here.
def index(request):
    return JsonResponse({'name': 'dev'},safe=False,status=201)


def login(request):
    data_values={}
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = MyUser.objects.filter(username=username,password=password)
        print(user)
        if user:
            query = list(MyUser.objects.filter(username=data['username']).values('uniq_id'))
            for v in query:
                print(v.get('uniq_id'))
                if user:
                    data_values = {'message': "Success", 'uniq_id': query[0]['uniq_id']}
                    return JsonResponse(data=data_values, safe=False)
                
        else:
            return JsonResponse({'message': 'wrong username or password'}, safe=False)
    else:
        JsonResponse({'message':'wrong method'})


def register(request):
    data_values={}
    if request.method == 'POST':
        data  = json.loads(request.body.decode("utf-8"))
        print(data)
        username = data['username']
        print(username)
        password = data['password']
        check=MyUser.objects.filter(username=data['username']).values('username')
        if check:
            return JsonResponse({'message':'username Existed'},safe =False,status=201)
        else:
            query = MyUser.objects.create(name=data['name'],username=data['username'], password=data['password'],email=data['email'],gender=data['gender'],mobile=data['mobile'])
            return JsonResponse({'message': 'successfully Inserted'}, safe=False, status=201)


def addCar(request):
    if request.method =='POST':
        print(request.body)
        data = json.loads(request.body.decode("utf-8"))
        user = MyUser.objects.get(uniq_id=data['addedBy'])

        # carnumber = CarDetails.object
        if user:
            query= CarDetails.objects.create(carname=data['carname'],carseats=data['carseats'],addedBy=user,carNumber =data['carnumber'] )
            if query:
                return JsonResponse({'message': 'Success'}, safe=False, status=201)
            else:
                return JsonResponse({'message': 'some error occured'}, safe=False, status=400)
        else:
            return JsonResponse({'message': 'User Doesnot Exist'}, safe=False, status=400)


def addPool(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        check_for_pooled = list(userPooling.objects.filter(userPooled=data['uniq_id'],status='ACTIVE'))
        if check_for_pooled:
            return JsonResponse({'message': 'User is already pooled'}, safe=False, status=201)
        else:
            check_for_car_user=list(CarDetails.objects.filter(carNumber=data['carNumber']).values('addedBy','cardetailsId'))
            if check_for_car_user[0].get('addedBy')==data['uniq_id']:
                print("chwbdsns,da,sn")
                check_for_one_pooling_before = list(startPooling.objects.filter(carPooled=check_for_car_user[0].get('cardetailsId'),pooledbyid=data['uniq_id'],status='INACTIVE'))
                if check_for_one_pooling_before:
                    print("chwbdsns,da,sn")
                    startPooling.objects.filter(carPooled=check_for_car_user[0].get('cardetailsId'),pooledbyid=data['uniq_id'],status='INACTIVE').update(time_start=data['time_start'],time_end = data['time_end'],latitude=data['latitude'],longitude=data['longitude'],status='ACTIVE',seats=data['carseats'])
                    return JsonResponse({'message': 'Successssfuly updated'}, safe=False, status=201)
                else:
                    user_pooling = MyUser.objects.get(uniq_id=data['uniq_id'])
                    myCar = CarDetails.objects.get(carNumber=data['carNumber'])
                    query=startPooling.objects.create(time_start=data['time_start'],time_end = data['time_end'],latitude=data['latitude'],longitude=data['longitude'],status='ACTIVE',carPooled=myCar,seats=data['carseats'],pooledbyid=user_pooling)
                    return JsonResponse({'message': 'Successssfully added'}, safe=False, status=201)
            else:
                return JsonResponse({'message': 'Car doesnot exist for given user'}, safe=False, status=201)
            

def profile(request):
    data_values = {}
    cars =[]
    if request.method =='GET':
        query = MyUser.objects.filter(uniq_id=request.GET['uniq_id']).values('name','username','password','gender','email','mobile')
        query2 = list(CarDetails.objects.filter(addedBy_id=request.GET['uniq_id']).values('carname','carseats','carNumber'))
        print(query)
        if list(query):
            cars.append({'userdata':query[0]})
            # return JsonResponse(data=data_values, safe=False, status=201)
        for q in query2:
            cars.append({'car':q})
        return JsonResponse(data=cars, safe=False, status=201)

def getAllDetails(request):
    data_values = {}
    details = []
    pooler_details = []
    pooled_details=[]
    user_details_poolers=[]
    if request.method == 'GET':
        query_check_user = MyUser.objects.get(uniq_id = request.GET['uniq_id'])
        if query_check_user:
            user_own_details = list(MyUser.objects.filter(uniq_id = request.GET['uniq_id']).values('name','username','mobile','email','uniq_id'))
            for a in user_own_details:
                details.append({'profile':a})
            check_pooling_details = list(startPooling.objects.filter(pooledbyid=request.GET['uniq_id'],status='ACTIVE').values('latitude','time_start','time_end','seats','longitude','carPooled','startPoolingId'))
            if check_pooling_details:
                for a in check_pooling_details:
                    # pooler_details.append({'trip_details':a})
                    car_details = list(CarDetails.objects.filter(cardetailsId=a.get('carPooled'),addedBy=request.GET['uniq_id']).values('carNumber','carseats','carname'))
                    # print(a.get('carPooled'))
                    if car_details:
                        for m in car_details:
                            a['car_details']=m
                            poolers_id=list(userPooling.objects.filter(status='ACTIVE',poolingwithid=a.get('startPoolingId')).values('userPoolingId','userPooled'))
                            # print(poolers[0].get('userPooled'))
                            details.append({'my_pooling_details':a})
                            if poolers_id:
                                for m in poolers_id:
                                    pooler_details = list(MyUser.objects.filter(uniq_id=m.get('userPooled')).values('name','username','mobile','gender','email'))
                                    user_details_poolers.append({'pooler':pooler_details[0]})
                                    # print(user_details_poolers)
                            a['poolers_details']=user_details_poolers
                            # details.append({'poolers_details':a})
            else:
                details.append({'my_pooling_details':pooler_details})
            check_isPooling_details = list(userPooling.objects.filter(userPooled=request.GET['uniq_id'],status='ACTIVE').values('poolingwithid'))
            if check_isPooling_details:
                get_pooling_details = list(startPooling.objects.filter(startPoolingId = check_isPooling_details[0].get('poolingwithid')).values('latitude','longitude','time_start','time_end','seats','pooledbyid'))
                if get_pooling_details:
                    for b in get_pooling_details:
                        get_pooler_details = list(MyUser.objects.filter(uniq_id=get_pooling_details[0].get('pooledbyid')).values('name','mobile','email'))
                        for a in get_pooler_details:
                            b['pooler']=a
                            details.append({'my_trip_details':b})
            else:
                details.append({'my_trip_details':pooled_details})

            return JsonResponse(data=details,safe=False,status=200)


def addUsertoPool(request):
    if request.method=='POST':
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        uniq = data['uniq_id']
        query_search = list(MyUser.objects.filter(uniq_id=uniq).values('uniq_id'))
        # print(query_search.get('uniq_id'))
        if query_search:
            query_car_id = list(CarDetails.objects.filter(carNumber=data['carNumber']).values('cardetailsId'))
            if query_car_id:
                query_search_seats = list(startPooling.objects.filter(carPooled=query_car_id[0].get('cardetailsId')).values('seats','startPoolingId'))
                print(query_search_seats[0].get('seats'))
                currentseat = query_search_seats[0].get('seats')
                if query_search_seats[0].get('seats')>1:
                    try:
                        search_already_pooled_once = userPooling.objects.filter(userPooled = data['uniq_id'] ).values('status')
                        if search_already_pooled_once[0].get('status') == 'ACTIVE':
                            return  JsonResponse({'message': 'User Already Pooled'}, safe=False, status=400)
                        elif search_already_pooled_once[0].get('status') == 'INACTIVE':
                            poolingwith = startPooling.objects.get(carPooled=query_car_id[0].get('cardetailsId'))
                            print("checkkkkk")
                            userPooling.objects.filter(userPooled=data['uniq_id']).update(status = 'ACTIVE',poolingwithid=poolingwith)
                            startPooling.objects.filter(carPooled=query_car_id[0].get('cardetailsId')).update(seats=currentseat-1)
                            return  JsonResponse({'message': 'User Successfully Updated'}, safe=False, status=200)
                    except:
                        add = MyUser.objects.get(uniq_id=uniq)
                        poolingwith = startPooling.objects.get(carPooled=query_car_id[0].get('cardetailsId'))
                        startPooling.objects.filter(carPooled=query_car_id[0].get('cardetailsId')).update(seats=currentseat-1)
                        userPooling.objects.create(status='ACTIVE',userPooled=add,poolingwithid = poolingwith)
                        return  JsonResponse({'message': 'User Successfully Pooled'}, safe=False, status=200)
                    
                return JsonResponse({'message': 'Seats Fulll'}, safe=False, status=400)
        else:
            return JsonResponse({'message': 'User Not found'}, safe=False, status=400)
    else:
        return JsonResponse({'message': 'Wrong Request type'}, safe=False, status=400)

def getcurrentPools(request):
    data_values = {}
    if request.method=='GET':
        query = list(userPooling.objects.filter(userPooled=request.GET['user_id']).values('status'))
        if len(query)!=0:
            data_values = {'status': query[0].get('status')}
            return JsonResponse(data=data_values, safe=False, status=200)
        else:
            cardetailid = CarDetails.objects.get(addedBy=request.GET['user_id'])
            print("hello")
            query3 = list(startPooling.objects.filter(carPooled=cardetailid).values('status'))
            if len(query3)!=0:
                print(query3)
                data_values = {'status': query3[0].get('status')}
                return JsonResponse(data=data_values, safe=False, status=200)
        # else:
        #     data_values = {'status': 'INACTIVE'}
        #     return JsonResponse(data=data_values, safe=False, status=200)

def endmypool(request):
    if request.method=='GET':
        check_for_active = list(userPooling.objects.filter(userPooled=request.GET['uniq_id'],status='ACTIVE').values('poolingwithid'))
        if check_for_active:
            query = userPooling.objects.filter(userPooled=request.GET['uniq_id']).update(status = 'INACTIVE')
            check_seats = startPooling.objects.filter(startPoolingId=check_for_active[0].get('poolingwithid')).values('seats')
            seats = check_seats[0].get('seats')
            query2 = startPooling.objects.filter(startPoolingId=check_for_active[0].get('poolingwithid')).update(seats=seats+1)
            if query and query2:
                return JsonResponse({'message': 'Successfully Endpool'}, safe=False, status=200)
            else:
                return JsonResponse({'message': ' Some error occured'}, safe=False, status=401)
        else:
            return JsonResponse({'message':'User is already inactive'},safe=False,status=400)
    else:
        return JsonResponse({'message':'Wrong Request Type'},safe=False,status=400)


def endpooledcar(request):
    if request.method=='GET':
        check_for_active_pooling = list(startPooling.objects.filter(status='ACTIVE',pooledbyid=request.GET['uniq_id']).values('startPoolingId'))
        if check_for_active_pooling:
            query_check_for_active_poolers = list(userPooling.objects.filter(poolingwithid=check_for_active_pooling[0].get('startPoolingId'),status='ACTIVE'))
            if query_check_for_active_poolers:
                return JsonResponse({'message':'User is pooling someone'},safe=False,status=400)
            else:
                query_update = startPooling.objects.filter(pooledbyid=request.GET['uniq_id'],status='ACTIVE').update(status='INACTIVE')
                return JsonResponse({'message': 'Successfully EndpooledCar'}, safe=False, status=200)
        else:
            return JsonResponse({'message':'User is already inactive'},safe=False,status=400)