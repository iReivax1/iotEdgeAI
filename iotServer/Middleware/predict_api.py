import os
import numpy as np
import tensorflow as tf
from datetime import datetime
import io
from flask import Flask,Blueprint,request,render_template,jsonify, abort
import Database.db as db
import sys
sys.path.append("/Users/xavier/Documents/NTU/CZ4171/Assignment/iotNN/")
# sys.path.append("/home/xavi0007/iotNN")
from plant_predict import main as predict_main
from jinja2 import TemplateNotFound


predict_blueprint = Blueprint('predict_blueprint',__name__,template_folder='./templates',static_folder='./Static')
UPLOAD_URL = '20.198.224.77/Static/'


@predict_blueprint.route('/')
def show():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@predict_blueprint.route('/predict' , methods=['POST'])
def predict():  
     if request.method == 'POST':       
        if 'file' not in request.files:
           return ("Error")
      
        user_file = request.files['file']    
        if user_file.filename == '':
            return ("404 file not found") 
       
        else:
            path = os.path.join(os.getcwd()+'/Static/'+user_file.filename)
            print(path)
            user_file.save(path)
            pred_class, score = predict_main(path)
            score = str(score)
            # db.add_new_image(
            #     user_file.filename,
            #     pred_class,
            #     score,
            #     datetime.now(),
            #     UPLOAD_URL+user_file.filename)
            print(user_file.filename,pred_class, score, datetime.now())
            return jsonify({
                "status":"success",
                "title": user_file.filename,
                "prediction":pred_class,
                "confidence":score,
                "upload_time":datetime.now()
                })
          

            

   




            
           
          

