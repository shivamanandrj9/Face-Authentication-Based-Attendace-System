from numba import jit
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from pytest import Instance
from userlogin.forms import Myform, imageform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from userlogin.models import *
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

def remove(name):
    yo = ""
    for i in range(len(name)):
        if (name[i] == '-' or name[i] == ' ' or name[i] == ':'):
            pass
        else:
            yo += str(name[i])
    return yo

client=pymongo.MongoClient("mongodb://localhost:27017/")

# @jit
def upload_webcam_mod(request):
    if request.method == 'POST':
        # print(form)

        aman = request.POST.get('data')
    #   cur=time.time()
        cur = datetime.datetime.now()
        cur = remove(str(cur))
        response = urllib.request.urlopen(aman)
        name = "D:\\new\Attendance_System-main\media\images\\"+cur
        filename = "%s.jpg" % name
        with open(filename, 'wb') as f:
            f.write(response.file.read())
        rawimage = face_recognition.load_image_file(filename)
        course_name=request.POST.get('course')
    try:
        now = datetime.datetime.now()
        year=now.strftime("%Y")
        month=now.strftime("%m")
        day=now.strftime("%d")
        date=year+'-'+month+'-'+day


        db=client.Face_Try
        collection=db.auth_user
        
        db2=client.attendance
        collection2=db2[date]

   
        total=image.objects.all()
        known_face_encodings=[]
        known_usermapid=[]
      
        for x in total:
            if x.facedata is None:
                continue
            known_face_encodings.append(x.facedata)
            print(known_face_encodings[0])

            # print(known_face_encodings[0])
            known_usermapid.append(x.user_map_id)
            # print(known_usermapid)
            

        all_face_locations = face_recognition.face_locations(rawimage, number_of_times_to_upsample=2,model='cnn')
        all_face_encodings=face_recognition.face_encodings(rawimage,all_face_locations)

        for current_face_location, current_face_encoding in zip(all_face_locations,all_face_encodings):
                print(current_face_encoding)
                if current_face_encoding is None:
                    continue
                
                all_matches=face_recognition.compare_faces(known_face_encodings,current_face_encoding,tolerance=0.6)
                if True in all_matches:
                    first_match_index=all_matches.index(True)
                    userid = known_usermapid[first_match_index]
                    
                    records=collection.find_one({'id':userid})



                    my_dict = {"user_map_id": userid,
                                "First Name": records["first_name"],
                                "Last Name" : records["last_name"],
                                "Email" : records["email"],
                                "Course" : course_name,
                                "Roll" :records["username"],
                                "Date_Time": now,
                                }

                    collection2.insert_one(my_dict)
                    
        messages.success(request, f'Your attendance was marked.')

    except:
        messages.warning(request, f'Face not captured. Try again')
    else:
        print("NULL")
    return render(request, 'userlogin/upload_webcam_modified.html')