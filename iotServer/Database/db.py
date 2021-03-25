from pymongo import MongoClient
from bson import ObjectId 

client = MongoClient("mongodb://20.198.224.77:27017")
db = client.image_prediction
image_details = db.imageData

def add_new_image(img_name,prediction_label,score,time,url):
    image_details.insert({
        "file_name":img_name,
        "prediction":prediction_label,
        "confidence":score,
        "upload_time":time,
        "url":url
    })
    
def get_all_image():
    return image_details.find()