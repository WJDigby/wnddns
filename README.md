wnddns.py

The intent of this script is to send an email to the user's gmail account when their public IP changes. The script would run on a home server, so when remote the user would know if their home IP has changed. Running the script should be automated through cron or a task scheduler.

The script makes use of the ipify API: https://www.ipify.org/

Code for initializing the Gmail API and sending email are taken from Gmail's API guide:
* https://developers.google.com/gmail/api/quickstart/python
* https://developers.google.com/gmail/api/guides/sending

Workflow is as follows:

#1. Cron job executes the script (set up outside this script)
#2. Script initializes the Gmail API object
#3. Script checks the current public IP using https://www.ipify.org
#4. Script compares current public IP with the stored (previous) public IP
#5. If IP has changed, script generates and sends an email with the updated IP.

