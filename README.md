# MQTT-program-runner
> Easy to configure program for running programs and commands according to MQTT messages.

Currently tested on Win10 only. Linux support will be added later.
This program provides a MQTT client that can run different commands when different messages arrive.

This program aims to be friendly to non tech savvy individuals by fulfilling the following:
- Has an option to run as .exe for portable use without additional install process needed.
- Very easy to configure.
- The configuration can be changed without restarting the program.
- Shows a tray icon with a menu and an Exit option.
- Desktop notification (toasts) can be disbled from the tray menu.

## Installation

Currently only supports Win10.

If you just want to run the program, no installation is required. just run the .exe in the main folder.

if you want to run the python script : 

```sh
pip install requiremrnts.txt
```

## Configuration

Before you start the program, you'll need to change the configuration according to your setup.

Configuration is done via the ``config.yaml`` file located in the data folder.

The file follows the YAML format, but it has a very basic structure that's easy to follow:

There are two sections for the file - config and commands.

### Config

The format of the config section is as follows:
```sh
config:
   topic: <string> topic to which the client will subscribe
   broker: <string> MQTT broker server IP
   port: <integer> MQTT broker server port
   browser_path: <string> The path to the web browser's executable. forward-slashes (/).
```

### Commands
   
The format of the commands section is as follows:
```sh
command:
   command_name: The name of the command. Must be unique.
       cmd_type: <string> The type of command, can be any of ["browser", "app", "cmd"]
       data: <string> Additional data needed to run the command.#                      for type: "browser" - The URL of the webpage to be opened
                      for type: "app" - The path to the application's executable. double-backslashes (\\).
                      for type: "cmd" - The command line to be executed in shell.
       icon: <string> [optional] The path to the icon to be displayed in notifications. If not included, the program's icon will be used.
       toast: <string> [optional] A custom message to be displayed when the command is triggered. If not included, a "<command_name> triggered" message will be displayed.
       message: <string> [optional] An alternate MQTT payload to be matched to trigger the command. If not included, <command_name> will be used.
```
NOTE: The path to the customized icon is relative to the icons folder.

There is an example for a config file in the data folder. Simply edit the file to fit your needs and system.

## Tray Menu 
	 
After running the program, a tray icon will appear.
Right click will open a menu with the following options:

+ Disable notifications for messages - Disables desktop notifications (toasts) from appearing when a command is triggered. NOTE: Notification will still show when reloading a YAML file fails.
+ Reload YAML - This allows to update the YAML file with new commands or chagne the MQTT topic and browser path without restarting the program. If the reload was unsuccessfull, a notification will appear. NOTE: when reloading YAML from the tray icon's menu, the 'broker' and 'port' parameters will NOT change in the current session. To change the MQTT server connection parameters, restart the program.
+ Exit - Terminate the program.

## Release History

* 0.0.1
    * Work in progress

## Contact info

Daniel Harari – daniel@harariprojects.com

http://HarariProjects.com

https://github.com/harari/MQTT-program-runner

## LISENCE

Distributed under the GNU GPLv3 license. See ``LICENSE`` for more information.