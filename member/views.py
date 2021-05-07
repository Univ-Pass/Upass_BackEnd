from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Member
from .serializers import MemberSerializer
from subprocess import Popen, PIPE, STDOUT 
from django.http import HttpResponse
import subprocess
import hashlib
import json
import os
import random
import base62
#import bcrypt
# Create your views here.


@csrf_exempt
def member_list(request):
    #모든 학생들 조회 or 새로운 학생 생성
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        studentDB = Member.objects.all()
        '''
        try:
            student = Member(
                major =data['major']
                stdnum = data['stdnum']
                name = data['name']
                email = data['email']
            )
        '''
        email = data['email']
        '''
        stdnum = data['stdnum']
        
        if studentDB.filter(email = email).exists() :
            return JsonResponse({'msg':'Email is already exists'}, status=400)
        elif studentDB.filter(stdnum = stdnum).exists() :
            return JsonResponse({'msg':'stdnum is already exists'}, status=400)
        '''

        #ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        salt = base62.encodebytes(os.urandom(16))
        salt = bytes(salt, encoding="utf-8")
        #for i in range(16):
        #    salt.append(random.choice(ALPHABET))

        #salt_string = "".join(salt)

        email_dump = json.dumps(email, sort_keys = True).encode()
        email_dump = email_dump + salt
        #print('salt_string = ')
        #print(salt_string)
        #print('email_dump = ')
        #print(email_dump)

        email_hash = hashlib.sha256(email_dump).hexdigest()
        email_data_json = { 'email_hash' : '' }
        email_data_json['email_hash'] = email_hash
        data['email_hash'] = email_hash

        serializer = MemberSerializer(data=data)


        #if pk == 'temporaryKey':         #app사용자인지 확인
        if serializer.is_valid():       #입력 data들 포맷 일치 여부 확인
            serializer.save()
            return JsonResponse(email_data_json, status=201)

        return JsonResponse(serializer.errors, status=400)       


@csrf_exempt
def member(request, word):
    #학생 수정
    obj = Member.objects.get(email=word)

    if request.method == 'GET':
        serializer = MemberSerializer(obj)
        return JsonResponse(serializer.data, status=201, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)   


@csrf_exempt
def run_python(request): 
    if request.method == 'GET': 
        command = ["sh","/home/caps/indy/start_docker/api.sh","f92f65a3731e","test@kyonggi.ac.kr"]
        try: 
            process = Popen(command, stdout=PIPE, stderr=STDOUT) 
#            output = process.stdout.read() 
#            exitstatus = process.poll() 
#            pwd = os.path.realpath(__file__)
            with open('/home/caps/indy/start_docker/data.json')as f:               
                json_data = json.load(f)
                email = json_data['email']
                did = json_data['did']
            
            '''
            if (exitstatus==0): 
                with open('./data.json')as f:
                    json_data = json.load(f)
                    email = json_data['email']
                    did = json_data['did']
            else: 
                result = {"status": "Failed  ", "output":str(output)}
                return JsonResponse({'msg':'exitstatus is not 0'}, status=400)
            '''
        except Exception as e: 
            result =  {"status": "failed_Exception"  , "output":str(e)} 
            return JsonResponse({'msg':'failed_Exception','erreor 내용':str(e),'pwd':pwd}, status=400)

        return JsonResponse(json_data, status=201)


@csrf_exempt
def readDID(request): 
    with open('../docker/Blockchain_Capstone_Indy/start_docker/data.json')as f:
        json_data = json.load(f)
        email = json_data['email']
        did = json_data['did']
    return JsonResponse(json_data, status=201)
