from flask import Flask, request, render_template,jsonify
import socket
import ast
import copy
import sys,os
import eventlet
from flask_socketio import SocketIO
global Ports
Ports=9003
# SAMPLE_SPREADSHEET_ID = '1kjqfjXV4bx_Mg48Q5XuTDreH4bZRMcvnwjL4JN6WaXw'
# SAMPLE_RANGE_NAME = 'Sheet1!A1:C24'
import pandas as pd
# sheet_id = SAMPLE_SPREADSHEET_ID 
global nfc_tag_content
nfc_tag_content='[1]'
# sheet_name = "pound_maker"
# url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
# df=pd.read_csv(url)
# d={}
# num_sensors=int(df.iloc[0,1])
# print("number of active alectrodes",num_sensors)
# for i in range(1,num_sensors+1):
#     for j in range(1,3):
#         d["url{0}_{1}".format(i-1,j)]=df.iloc[i,j]
#         print("url{0}_{1}".format(i-1,j))
#         print(df.iloc[i,j])
SAMPLE_SPREADSHEET_ID = '1AGFe0ZvGIjwm5txlaFqmfurk-PU70sTBWPxspqwvooc'
SAMPLE_RANGE_NAME = 'Sheet1!A1:C24'
import pandas as pd
sheet_id = SAMPLE_SPREADSHEET_ID 
sheet_name = "page_access"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
df_father=pd.read_csv(url,header=0)
selected_page=df_father["your selection"][0]
number_of_listed_pages=df_father["number of listed pages"][0]
print("number of active pages",number_of_listed_pages,"your selection",selected_page)

sheet_name_new=df_father["sheet_name"][selected_page]
url_second_page=f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name_new}"

d={}
df=pd.read_csv(url_second_page)
num_sensors=int(df.iloc[0,1])
print("number of active alectrodes",num_sensors)
for i in range(1,num_sensors+1):
    for j in range(1,3):
        d["url{0}_{1}".format(i-1,j)]=df.iloc[i,j]
        print("url{0}_{1}".format(i-1,j))
        print(df.iloc[i,j])


async_mode = None
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path) 

if getattr(sys, 'frozen', False):
    template_folder =resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
templateData = {
      'title' : 'Welcome to the heritage project!',
      }
socketio = SocketIO(app, async_mode=async_mode)
thread = None
# thread_lock = Lock()
def my_function_play_for_all(url,url_2,index):

    global URL
    global URL2
    global Stop
    global flag_url
    Stop=0
    
    URL=url
    URL2=url_2
    print("pin %s is activated"%(index))
    print(URL)
    flag_url=1
def get_ip_address():
 ip_address = ''
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 print(ip_address)
 s.close()
 return ip_address
# app = Flask(__name__)
def run_app():
    global Ports
    # app.run(host=get_ip_address(), port=9003,debug=False,threaded=True)
    # eventlet.wsgi.server(eventlet.listen((get_ip_address(), 9003)), app)
    eventlet.wsgi.server(eventlet.listen((get_ip_address(), Ports)), app)
    # app.run(host=get_ip_address(), port=9003,debug=False,threaded=True) 
    # socketio.run(app,host=get_ip_address(), port=9003)
@app.route('/')
def index():
    global URL
    global URL2
    global Stop
    global Ports
    # print("passed url",URL)
    # Read Sensors Status
    # buttonSts = GPIO.input(button)
    # senPIRSts = GPIO.input(senPIR)
    # stopSts = GPIO.input(stop)
    templateData = {
      'title' : 'Welcome to the heritage project!',
      'main_page':"http://"+get_ip_address()+':'+str(Ports)
      }

    # webbrowser.open_new(URL)
    print("http://"+get_ip_address()+':'+str(Ports))
   
    # return render_template('index.html',**templateData)
    return render_template('index.html',**templateData)
# @app.route('/update_variable')
# def update_variable():
#     if flag_url==1:
#         new_value = (copy.deepcopy(URL))
#         return jsonify(new_value=new_value,Flag=1)
#     else:
#         return jsonify(new_value='',Flag=0)
@app.route('/requests',methods=['POST','GET'])
def tasks():                     
                 
    if request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

@app.route('/update_variable', methods=['POST'])
def save_nfc_tag_content():
    global nfc_tag_content
    nfc_tag_content = request.data.decode('utf-8')
    # Perform desired operations with the NFC tag content
    print(f"Received NFC tag content: {nfc_tag_content}")
    return 'Success'
@app.route('/update_variable2')
def update_variable():
    global nfc_tag_content
    # from urllib.parse import urlparse
    data = nfc_tag_content  # Get the data from the request and decode it
    # print("Received data:", data) 
    # data=urlparse(data)
    data = ast.literal_eval(data)
    print("Received data integer",data[0])
    if data!='':
        print("Received data:", data[0]) 
        # my_function_play_for_all(d["url{0}_{1}".format(i,1)],d["url{0}_{1}".format(i,2)],i)
        try:
            new_value = (copy.deepcopy(d["url{0}_{1}".format(data[0],1)]))
            print("new_value",new_value)
            return jsonify(new_value=new_value,Flag=1)
        except:
            pass
    else:
        return jsonify(new_value='',Flag=0)
if __name__ == '__main__':
    run_app()
