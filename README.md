# IPtoGmail

This python script has two main purposes:

  1st: Get your public IPv4 \n
  2ns: Send your new public IPv4 as an email (using Gmail) in case that it has changed
 
For this implementation, we use the Gmail API which can be see in more detail <a href="https://developers.google.com/gmail/api/quickstart/python">here</a>

It is important that you must have a 'Credentials.json' file in the folder where you have placed the python file. This file must eb obtained using the Gmail API vía the <a href="https://console.cloud.google.com/apis/library">Google API Library</a>. This is a very simple process but the most important one.

Once you got this file, then you start the script using the python compiler, it will prompt a web window with the Google OAuth2 page in order to give the code the neccesarry permissions for sending emails via your gamil account. This process must be done at least one time. Once you do this for the first time, a file in your computer calle 'Token.json' will be stored which will be used for the next executions to avoid sign in every time you execute the script.

Remember you must change the commented code on the line 110, where you must place your email and the email where you want to send the mail.

Another file called ips.json will be automatically created the first time you run the script in order to make the persistance layer of the application. This file will only store the new IP found and the last IP that you have.

I personally use this script in a Raspberry Pi running Raspbian, with a scheduled CRON every day.

If you need any help with this script or want to ask some doubt I will be glad to help you in anything I could.

