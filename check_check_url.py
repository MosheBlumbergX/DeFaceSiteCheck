import sys
import os.path
import urllib2
import requests
import smtplib

def sendmail(t=" ",c=" ",r=" "):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    list =[c,r]
    body = '\n'.join(list)
    msg = "\r\n".join([
      "From: from@gmail.com",
      "To: to@hotmail.co.uk",
      "Subject: Web Page Alert",
      "",
      t + c + " " + r # this is the body
      ])
    
    mail.ehlo()
    mail.starttls()
    mail.login('fromemail','pass')  # gmail login and pass 
    mail.sendmail('from','to',msg)  # mail.sendmail('fromemail','toemail',msg)
    mail.quit


url = 'http://www.iana.org/domains/example/'
#url = "https://google.com"

saved_time_file = 'last_time_check.txt'

request = urllib2.Request(url)
if os.path.exists(saved_time_file):
    """ If we've previously stored a time, get it and add it to the request"""
    last_time = open(saved_time_file, 'r').read()
    request.add_header("If-Modified-Since", last_time)

try:
    response = urllib2.urlopen(request) # Make the request
except urllib2.HTTPError, err:
    c = str(err.code)
    r = str(err.reason)
    if err.code == 304:
        #print "Nothing new."
        sys.exit(0)
    else: 
        t = "There was an error on the page that is not expected: "
        sendmail(t,c,r)
        sys.exit(0)
        
request = urllib2.Request(url)
response = urllib2.urlopen(request)

last_modified = response.info().get('Last-Modified', False)
if last_modified:
    open(saved_time_file, 'w').write(last_modified)
else:
    pass # write code if you want to check something else

t = "Something has changed "
sendmail(t)
