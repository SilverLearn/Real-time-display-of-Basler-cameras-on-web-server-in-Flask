#Created by : Mohammad Abdollahi
import argparse
import io
import os
from PIL import Image
import matplotlib.pyplot as plt # for ploting the scanned line
import pandas as pd
import imutils
from numpy import asarray
from numpy import savetxt
import cv2
import numpy as np
import pypylon.pylon as py
from datetime import datetime
from gevent.pywsgi import WSGIServer
import torch
from flask import Flask, render_template, request, redirect, Response
from selenium import webdriver
import math
app = Flask(__name__)


from io import BytesIO
first_device = py.TlFactory.GetInstance().CreateFirstDevice()
icam = py.InstantCamera(first_device)
icam.Open()
icam.PixelFormat = "BGR8"
def gen():

  while True:
        image = icam.GrabOne(4000) ### 4ms time for grabbing image 
        image = image.Array
        image = cv2.resize(image, (0,0), fx=0.8366, fy=1, interpolation=cv2.INTER_LINEAR)### 2048x2048 resolution or INTER_AREA  inter_linear is fastest for and good for downsizing 
        ret, jpeg = cv2.imencode('.jpg', image)    
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type:image/jpeg\r\n'
               b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
               b'\r\n' + frame + b'\r\n')

    
@app.route('/exposure', methods=['GET', 'POST'])
def exposure():
    ss = icam.ExposureTime.Value
    max = icam.ExposureTime.GetMax()
    if request.method == 'POST':
       # print(request.form.get('text_exposure'))
        r = int(request.form.get('text_exposure'))
        if r<max:
         icam.ExposureTime.SetValue(r)
         ss = icam.ExposureTime.Value
    return render_template('index.html',result = ss, max = max)
#-----------------------------------------------------------------
    
@app.route('/width1', methods=['GET', 'POST'])
def width1():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_width'))
        print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc()
        
    icam.Width.SetValue(r)
    current_w  = icam.Width.GetValue()
    return render_template('index.html',current_w = current_w)
#-----------------------------------------------------------------

#-----------------------------------------------------------------
    
@app.route('/height1', methods=['GET', 'POST'])
def height1():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_height'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.Height.SetValue(r)
    return render_template('index.html')
#-----------------------------------------------------------------
#-----------------------------------------------------------------
    
@app.route('/blacklevel', methods=['GET', 'POST'])
def blacklevel():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_blacklevel'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.BlackLevel.SetValue(r)
    return render_template('index.html')

    
@app.route('/gamma', methods=['GET', 'POST'])
def gamma():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_gamma'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.Gamma.SetValue(r)
    return render_template('index.html')
#-----------------------------------------------------------------
@app.route('/offsetx', methods=['GET', 'POST'])
def offsetx():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_offsetx'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.OffsetX.SetValue(r)
    return render_template('index.html')
#-----------------------------------------------------------------
#-----------------------------------------------------------------
@app.route('/offsety', methods=['GET', 'POST'])
def offsety():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_offsety'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.OffsetY.SetValue(r)
    return render_template('index.html')
#-----------------------------------------------------------------
#-----------------------------------------------------------------
@app.route('/gain', methods=['GET', 'POST'])
def gain():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_gain'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.Gain.SetValue(r)
    index()
    return render_template('index.html')
#-----------------------------------------------------------------
#-----------------------------------------------------------------
@app.route('/digital', methods=['GET', 'POST'])
def digital():
    if request.method == 'POST':
        #print(icam.Width.GetMin())
        r = int(request.form.get('text_digital'))
        #print(r)
       # new_width = icam.Width.GetValue() - icam.Width.GetInc() 
    icam.DigitalShift.SetValue(r)
    return render_template('index.html')
#-----------------------------------------------------------------
@app.route('/')
def index():
    current_w  = icam.Width.GetValue()
    max_w = icam.Width.GetMax()
    min_w = icam.Width.GetMin()
    current_h  = icam.Height.GetValue()

    max_h = icam.Height.GetMax()
    min_h = icam.Height.GetMin()
    
    current_offx  = icam.OffsetX.GetValue()
    max_ox = icam.OffsetX.GetMax()
    min_ox = icam.OffsetX.GetMin()
    
    current_offy  = icam.OffsetY.GetValue()
    max_oy = icam.OffsetY.GetMax()
    min_oy = icam.OffsetY.GetMin()
    current_g  = icam.Gain.GetValue()
    max_g = icam.Gain.GetMax()
    min_g = icam.Gain.GetMin()
    current_b  = icam.BlackLevel.GetValue()
    max_b = icam.BlackLevel.GetMax()
    min_b = icam.BlackLevel.GetMin()
    current_gamma  = icam.Gamma.GetValue()
    max_gamma = round(icam.Gamma.GetMax(), 2)
    min_gamma = icam.Gamma.GetMin()
    current_digital  = icam.DigitalShift.GetValue()
    max_digital = icam.DigitalShift.GetMax()
    min_digital = icam.DigitalShift.GetMin()
    current_exp  = icam.ExposureTime.GetValue()
    max_exposure = icam.ExposureTime.GetMax()
    min_exposure = icam.ExposureTime.GetMin()
    return render_template('index.html',max_w = max_w,min_w = min_w , max_h = max_h, min_h = min_h,
    max_ox = max_ox, min_ox = min_ox , max_oy = max_oy, min_oy = min_oy,
    max_g = max_g,min_g = min_g, min_b = min_b , max_b = max_b,
    max_gamma = max_gamma , min_gamma = min_gamma,max_digital = max_digital, min_digital = min_digital,
    max_exposure = max_exposure,min_exposure = min_exposure , current_w = current_w , current_exp = current_exp
    ,current_h = current_h , current_g = current_g , current_digital = current_digital , current_gamma = current_gamma,
    current_b = current_b , current_offx = current_offx , current_offy = current_offy)

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    '''
    model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
    ).autoshape()  # force_reload = recache latest code
    model.eval()
    '''
    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat