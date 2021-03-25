# Getting Started

## Client
The Client is done using flutter so it works on both iOS (need xcode) and Android
src files are mainly in ~/iotClient folder

## Deep neural network
Training logs is in ~/iotNN/output.txt
To train a model use classifier.
Uses open sourced dataset 

'''' citation = 
@ONLINE {beansdata,
    author="Makerere AI Lab",
    title="Bean disease dataset",
    month="January",
    year="2020",
    url="https://github.com/AI-Lab-Makerere/ibean/"
}
'''

## Start Azure server
Go to Azure and press start
## Start flask server
src files are in ~/iotServer folder
sudo su
source ./venv/bin/activate
cd iotServer
python3 server.py

Remember to change IP address and directories in server.py, predict_api.py, plant_predict.py