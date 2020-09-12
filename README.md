# Square-Digital-Download-Workflow
This was written as a way to support a digital download on a square site. The download was for a quilt pattern, and we wanted to have the pattern automatically sent out upon purchase with no input from us. This is the resulting proof of concept script. This is running on a VM on a Proxmox server. Since this is a proof of concept and minimum viable product, the code isn't the cleanest and it could use some work to make it more robust.

# Installing
This application relies on python 3 and pip3
```
pip3 install -r requirements.txt
```

# Using
  * Update the variables in the script (to be updated in the future)
  * create a new crontab with the settings
```
*/5 * * * * python3 /path/to/script/main.py >>/path/to/log/distro.log
```
  * This will run the script every 5 minutes, checking for new orders and sending emails for them


# Contributing
Contributions are welcome, submit a pull request and we'll take a look.
