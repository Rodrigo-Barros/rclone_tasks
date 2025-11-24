# Rclone tasks
This little script was born with purpose to solve my needs of sync multiple folders with multiple cloud
providers to make my backup process better.

# Examples
Given rclone_tasks.json file
```json
[
  {
    "enabled" : true,
    "command": "copy",
    "args": [
      "--verbose"
    ],
    "source": "~/.var/app/com.belmoussaoui.Authenticator/data/authenticator",
    "destination": [
      "GoogleDriveCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator",
      "DropboxCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator",
      "OnedriveCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator"
    ]
  },
]
```
 and running this command: `./rclone_tasks.py -f ./rclone_tasks.json`

 this produces the follwing commands:

 ```sh
/usr/bin/rclone copy /home/rodrigo/.var/app/com.belmoussaoui.Authenticator/data/authenticator GoogleDriveCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator --verbose
/usr/bin/rclone copy /home/rodrigo/.var/app/com.belmoussaoui.Authenticator/data/authenticator DropboxCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator --verbose
/usr/bin/rclone copy /home/rodrigo/.var/app/com.belmoussaoui.Authenticator/data/authenticator OnedriveCriptografado:/Flatpaks/.var/app/com.belmoussaoui.Authenticator/data/authenticator --verbose
 ```

 You can also debug this file with this command: `./rclone_tasks.py -f ./rclone_tasks.json -n`
