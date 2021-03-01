from flask import Flask,render_template,jsonify,Blueprint
mod = Blueprint('api',__name__,template_folder='./FrontEnd')
import iotServer.database as db
from bson.json_util import dumps

@mod.route('/')
def api():
    return dumps(db.get_all_image())