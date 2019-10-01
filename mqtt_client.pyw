import paho.mqtt.client as paho
import sys
import webbrowser
import subprocess
from pystray import MenuItem as item
import pystray
from PIL import Image
from win10toast import ToastNotifier
import cerberus
import yaml

# Gloabal Variables

exit_flag = False
notification_flag = True

data_folder_prefix = "data/"
icons_folder_prefix = "icons/"
icon_path = "icon.ico"
config_file = "config.yaml"
default_toast_suffix = " triggered"
data = []

# MQTT callbacks

def on_subscribe(client, userdata, mid, granted_qos):
	print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
	global icon_path
	global default_toast_suffix
	notification_title = "MQTT message received"
	notification = ""
	icon = ""
	toast = ""
	message = msg.payload.decode("ASCII")
	print("RECEIVED "+msg.topic+" "+str(msg.qos)+" payload:"+str(message))
	for item in data['commands']:
	
		#match with received message
		if 'message' in data['commands'][item]:
			if message != data['commands'][item]['message']:
				continue
		elif message != item:
			continue
		
		#set icon
		icon = icons_folder_prefix + data['commands'][item].get('icon', icon_path)
		
		#set toast
		toast = data['commands'][item].get('toast', default_toast_suffix)
			
		#execute
		type = data['commands'][item]['cmd_type']
		if type == "browser":
			webbrowser.get(data['config']['browser_path'] + " %s").open(data['commands'][item]['data'], 2)
		elif type == "app" or type == "cmd":
			subprocess.Popen(data['commands'][item]['data'].replace("\\", "\\\\"))
			
		#display toast
		if (notification_flag):
			toaster = ToastNotifier()
			toaster.show_toast(notification_title,
					   toast,
					   icon,
					   duration=5,
					   threaded=True)
					   
		break
		
def on_connect(client, userdata, flags, rc):
	print("CONNACK received with code %d." % (rc))
	client.subscribe(data['config']['topic'], qos=1)
	
# Helper Functions

def load_yaml():
	global data
	schema = {'config': 
				{'type': 'dict',
				'required': True,
				'schema': {
					'topic': {'type': 'string', 'required': True},
					'broker': {'type': 'string', 'required': True},
					'port': {'type': 'integer', 'required': True},
					'username': {'type': 'string', 'required': False},
					'password': {'type': 'string', 'required': False},
					'browser_path': {'type': 'string', 'required': True}
					}
				},
			  'commands':
				{'type': 'dict',
				 'required': True,
				 'keysrules': {'type': 'string'},
				 'valueschema'	: {
						'type': 'dict',
						'schema': {
							'cmd_type': {'type': 'string', 'required': True},
							'data': {'type': 'string', 'required': True},
							'icon': {'type': 'string', 'required': False},
							'toast': {'type': 'string', 'required': False},
							'message': {'type': 'string', 'required': False}
							}
					}
				}
			}
	v = cerberus.Validator(schema)
	
	with open(data_folder_prefix + config_file, 'r') as file:
		data = yaml.safe_load(file)
		
	if not v.validate(data):
		print("Error validating YAML")
		print(v.errors)
		toaster = ToastNotifier()
		toaster.show_toast("Error validating YAML",
				   "Restart program and try again",
				   icon_path="icon.ico",
				   duration=5,
				   threaded=True)
		return -1

# Pystray Callbacks	
	
def toggle_notification():
	global notification_flag
	notification_flag = not notification_flag
	
def exit_program(icon):
    global exit_flag
    exit_flag = True
    icon.stop()
	
def callback(icon):
    global exit_flag
    global data
	
    rc = load_yaml()
    if rc == -1:
        icon.stop()
        return
		
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_connect = on_connect
	
    if 'username' in data['config']:
        pw = ''
        if 'password' in data['config']:
            pw = data['config']['password']
        else:
            pw = None
        client.username_pw_set(data['config']['username'], pw)
			
    client.connect(data['config']['broker'], data['config']['port'])
    while True:
        client.loop(.1)
        if (exit_flag):
            print("Exiting MQTT thread")
            return

# Main
			
image = Image.open(icons_folder_prefix + icon_path)
menu = pystray.Menu(item('Disable notifications for messages', toggle_notification, checked=lambda item: not notification_flag),item('Reload Yaml', load_yaml), item('Exit', exit_program))
icon = pystray.Icon("MQTT client", image, "MQTT Client", menu)
icon.visible = True
icon.run(setup=callback)