from flask import Flask
app = Flask(__name__)
#defining a baseroute
@app.route('/')
def index():
    return 'Hello world'
if __name__ == '__main__':
    app.run(debug=True, port=80, host='10.0.0.4')