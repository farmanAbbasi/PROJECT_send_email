from bs4 import BeautifulSoup
import requests
import os
from flask import Flask
from flask import request
app = Flask(__name__)
import json
import smtplib
from email.message import EmailMessage
import urllib.request
import io

EMAIL=os.environ['email']
PASS=os.environ['password']

def sendEMail(data):
        to=data['to']
        subject=data['subject']
        body_heading=data['body_heading']
        body=data['body']
        pic=data['pic']

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL
        msg['To'] = to
        msg.set_content(body_heading)
        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
        <style>
            body{
            margin:0px;
            padding:0px;
            font-style: oblique;
            }
                .parent{
            position:relative;
            }
            img{
            padding:0;
            opacity:0.5
            }
            
            .child{
            position:absolute;
            padding:20px;
            top:0;
            left:0;
            bottom:0;
            right:0;
            }
        </style>
            <body>
            <div class="parent">
             <img src=""" +pic+ """ width=100%>
            </div>
            <div class="child">
            <h2>"""+body_heading+""" </h2>
            <p>"""+body+"""</>
            </div>
            
            </body>
        </html>
        """, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASS)
            smtp.send_message(msg)
        return "success"
  
   
    

@app.route('/sendMail', methods=['POST'])
def sendMail():
    data=request.get_json()
    r=sendEMail(data)
    if r=="success":
        return json.dumps({"message": "Message sent successfully"})
    return json.dumps({"message": "Failed"})

@app.route('/', methods=['GET'])
def getData():
    return json.dumps({"msg": "hello-m"})   


if __name__ == '__main__':
    app.run()
    

    
        
