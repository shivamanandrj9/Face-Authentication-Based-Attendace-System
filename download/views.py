from django.http import HttpResponse
from django.shortcuts import render, redirect
# from pytest import Instance
from userlogin.forms import Myform, imageform
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import cv2
import face_recognition
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib
import json
from urllib.request import urlopen
import tempfile
from binascii import a2b_base64
import datetime
import time
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import pymongo
import datetime
import pandas as pd

client=pymongo.MongoClient("mongodb://localhost:27017/")


def down(request):
    if request.method=="POST":
        cc=request.POST.get('course')
        date=request.POST.get('date')
        
        db=client.attendance
        
        collection=db[date]
        now = datetime.datetime.now()
        filename=now.strftime("%d%m%Y%H%M%S")
        filename=cc+filename
        all_records=collection.find({'Course':cc})
        print(all_records)
        
        list_cursor=list(all_records)
        df=pd.DataFrame(list_cursor)
        df = df.iloc[: , :-1]
        df.to_excel(r'' +filename+'.xlsx')
        
        
       
    return render(request,'userlogin/download.html')

def studdown(request):
    if request.method=="POST":
        date=request.POST.get('date')
        cc=request.user.username    
        db=client.attendance
        
        collection=db[date]
        now = datetime.datetime.now()
        filename=now.strftime("%d%m%Y%H%M%S")
        filename=cc+filename
        all_records=collection.find({'Roll':cc})
        print(all_records)
            
        list_cursor=list(all_records)
        df=pd.DataFrame(list_cursor)
        df = df.iloc[: , :-1]
        df.to_excel(r'' +filename+'.xlsx')
       
    return render(request,'userlogin/studdown.html')
    

