from flask import Flask
from Middleware.predict_api import predict_blueprint
import sys

app = Flask(__name__)
app.register_blueprint(predict_blueprint,  url_prefix='/')

if __name__ == '__main__':
    sys.path.insert(0, "/Users/xavier/Documents/NTU/CZ4171/Assignment/iotServer/Middleware/")
    sys.path.insert(0, "/Users/xavier/Documents/NTU/CZ4171/Assignment/iotServer/Database/")
    # sys.path.insert(0, "/home/xavi0007/iotServer/Database")
    # sys.path.insert(0, "/home/xavi0007/iotServer/Middleware")
    
    # app.run(debug=True, port=80, host='10.0.0.4')
    app.run(debug=True, port=80, host='127.0.0.1')
