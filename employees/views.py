from django.shortcuts import render,redirect
import requests
from datetime import datetime
from django.conf import settings
from requests import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import EmployeeSerializer
from .models import Employee,ActivityLogs
from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@api_view(["GET"])
@csrf_exempt
def employee_list(request):
    if request.method == 'GET':
        employees = Employee.objects.filter(is_deleted =False)
        employees_serializers = EmployeeSerializer(employees,many=True)

    return JsonResponse(employees_serializers.data, safe=False,status=status.HTTP_200_OK)

@api_view(["POST"])
@csrf_exempt
def add_employee(request):
    pload = json.loads(request.body)
    try:
        employee = Employee.objects.create(
            first_name = pload['first_name'],
            last_name = pload['last_name'],
            email = pload['email'],
            phone= pload['phone'],
            job_title = pload['job_title'],
            gender = pload['gender']
        )
        serializer = EmployeeSerializer(employee)
        return JsonResponse({'employee':serializer.data},safe=False,status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error':'Something terrible happened'}, safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
def update_employee(request,id):
    pload = json.loads(request.body)
    try:
        employee = Employee.objects.filter(id=id)
        employee.update(**pload)
        employee_data = Employee.objects.get(id=id)
        serializer = EmployeeSerializer(employee_data)
        return JsonResponse({'employee':serializer.data},safe=False,status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
def employee_delete(request,id):
    if request.method == 'GET':
        try:
            employee = Employee.objects.filter(id=int(id)).first()
            data = {"is_deleted":1}
            serializer = EmployeeSerializer(employee,data=data,partial=True)
            if serializer.is_valid():
                if serializer.update(employee,data):
                    return JsonResponse({'Delete successful!':serializer.data},safe=False,status=status.HTTP_204_NO_CONTENT)
                return JsonResponse(serializer.errors,safe=False,status=status.HTTP_304_NOT_MODIFIED)
            return JsonResponse(serializer.errors,safe=False ,status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def home(request):
    response  = requests.get('http://127.0.0.1:8000/employees/list')
    employees = response.json()
    # for e in employees:
    #     print(e)
    return render(request,'employees/home.html',{'employees':employees})
def create(request):
   return render(request,'employees/create.html')

def store(request):
    if request.method == 'POST':
        employee  = request.POST
        employee_data = json.dumps({'first_name':employee.get('first_name'),'last_name':employee.get('last_name'),'email':employee.get('email'),'phone':employee.get('phone'),'job_title':employee.get('job_title'),'gender':int(employee.get('gender'))})
        resp = requests.post('http://127.0.0.1:8000/employees/create',data=employee_data,headers={'Content-Type': 'application/json; charset=utf8'})
        ActivityLogs.objects.create(
            activity_name='create new usser',
            activity_time = datetime.now(),
            activity_request = request.POST,
            activity_response = resp.status_code,
            user = 1
        )
        return render(request,'employees/create.html')

def archive(request,id):
    if request.method  == 'GET':
        resp = requests.get('http://127.0.0.1:8000/employees/delete/'+id)
        ActivityLogs.objects.create(
            activity_name='Deleted usser',
            activity_time=datetime.now(),
            activity_request={'Archive user':id},
            activity_response=resp.status_code,
            user=1
        )
    return redirect('/employees/')

def update(request,id):
    employee = Employee.objects.filter(id=id).first()
    return render(request,'employees/update.html',{'employee':employee})
def store_update(request,id):
    if request.method == 'POST':
        employee = request.POST
        data = json.dumps({'first_name':employee.get('first_name'),'last_name':employee.get('last_name'),'email':employee.get('email'),'phone':employee.get('phone'),'job_title':employee.get('job_title'),'gender':int(employee.get('gender'))})
        # print(int(employee.get('gender')))
        resp = requests.put('http://127.0.0.1:8000/employees/update/'+id, data=data,headers={'Content-Type': 'application/json; charset=utf8'})
        ActivityLogs.objects.create(
            activity_name='Update usser',
            activity_time=datetime.now(),
            activity_request={'Update user': id},
            activity_response=resp.status_code,
            user=1
        )
        return redirect('/employees/')


def getlogs(response):
    logs = ActivityLogs.objects.all().values()
    for i in logs :
        print(i)
    return render(response,'employees/logs.html',{'logs':logs})