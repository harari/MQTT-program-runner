# MQTT-program-runner
> Easy to configure program for running programs and commands according to MQTT messages.

Currently tested on Win10 only. Linux support will be added later.
This program provides a MQTT client that can run different commands when different messages arrive.

This program aims to be friendly to non tech savvy individuals by fulfilling the following:
- Has an option to run as .exe for portable use without additional install process needed.
- Very easy to configure.
- The configuration can be changed without restarting the program.
- The configuration can be changed without requiring programming skills.
- Shows a tray icon with a menu and an Exit option.
- Desktop notification (toasts) can be disbled from the tray menu.

![](header.png)

## Installation

Currently only supports Win10.
If you just want to run the program, no installation is required. just run the .exe in the main folder.

if you want to run the python script : 

```sh
pip install requiremrnts.txt
```

## Usage example

Before you start the program, you'll need to change the configuration according to your setup.
Configuration is done via the config.yaml file locaten in the data folder.
The file follows the YAML format, but it has a very basic structure that's easy to follow:
There are two sections for the file - config and commands.

The format of the config section is as follows:
config:
   topic: <string> topic to which the client will subscribe
   broker: <string> MQTT broker server IP
   port: <integer> MQTT broker server port
   browser_path: <string> The path to the web browser's executable. forward-slashes (/).

The format of the commands section is as follows:
command:
   command_name: The name of the command. Must be unique.
       cmd_type: <string> The type of command, can be any of ["browser", "app", "cmd"]
       data: <string> Additional data needed to run the command.#                      for type: "browser" - The URL of the webpage to be opened
                      for type: "app" - The path to the application's executable. double-backslashes (\\).
                      for type: "cmd" - The command line to be executed in shell.
       icon: <string> [optional] The path to the icon to be displayed in notifications. If not included, the program's icon will be used.
       toast: <string> [optional] A custom message to be displayed when the command is triggered. If not included, a "<command_name> triggered" message will be displayed.
       message: <string> [optional] An alternate MQTT payload to be matched to trigger the command. If not included, <command_name> will be used.

There is an example for a config file included.
	   
NOTE: when reloading YAML from the tray icon's menu, the 'broker' and 'port' parameters will NOT change in the current session.
      to change the MQTT server connection parameters, restart the program.

After running the program, a tray icon will appear.
Right click will open a menu with the following options:

+ Disable notifications for messages - Disables desktop notifications (toasts) from appearing when a command is triggered. NOTE: Notification will still show when reloading a YAML file fails.
+ Reload YAML - This allows to update the YAML file with new commands or chagne the MQTT topic and browser path without restarting the program. If the reload was unsuccessfull, a notification will appear.
+ Exit - Terminate the program.

## Release History

* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## Contributing

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki