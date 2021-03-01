import os
import numpy as np
import tensorflow as tf
from datetime import datetime
import io
from flask import Flask,Blueprint,request,render_template,jsonify
import iotServer.database as db
from iotNN.plant_predict import main as predict


mod = Blueprint('backend',__name__,template_folder='./FrontEnd',static_folder='./Static')
UPLOAD_URL = '20.198.224.77/Static/'


@mod.route('/')
def home():
    return render_template('index.html')

@mod.route('/predict' ,methods=['POST'])
def predict():  
     if request.method == 'POST':       
        if 'file' not in request.files:
           return ("Error")
      
        user_file = request.files['file']    
        if user_file.filename == '':
            return ("404 file not found") 
       
        else:
            path = os.path.join(os.getcwd()+'\\Static\\'+user_file.filename)
            user_file.save(path)
            pred_class, score = predict(path)
            db.add_new_image(
                user_file.filename,
                pred_class,
                score,
                datetime.now(),
                UPLOAD_URL+user_file.filename)

            return jsonify({
                "status":"success",
                "prediction":pred_class,
                "confidence":score,
                "upload_time":datetime.now()
                })
          

            

   




            
           
          

