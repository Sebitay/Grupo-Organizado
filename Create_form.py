from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from datetime import date, timedelta
from email.message import EmailMessage
import smtplib
import ssl
import json

# email details
sender_email = 'seba123612@gmail.com'
sender_password = 'kkaupfbklzumzfgs'
receiver_email = 'seba123612@gmail.com'
subject = 'Link grupo organizado'
body = ''

# Load the saved credentials from the token file
with open('token.json', 'r') as token:
    credentials = Credentials.from_authorized_user_info(info=json.load(token))

# Set up the Drive and Forms APIs
drive_service = build('drive', 'v3', credentials=credentials)
forms_service = build('forms', 'v1', credentials=credentials)

# Gets form ID
formid=open('formid.txt','r')
for line in formid:
    id=line

# Deletes form
Delete_form = drive_service.files().delete(fileId=id).execute()

# Fecha
hoy=date.today()
manana= hoy + timedelta(1)
fecha=str(manana).split('-')
fecha_nueva=str(fecha[2])+'-'+str(fecha[1])+'-'+str(fecha[0])
nombre='Lista grupo organizado '+ fecha_nueva
 
# Create a file in Google Drive to represent the form
file_metadata = {
    'name': nombre,
    'parents': ['10LAXjho5wXNI5SvPp0OF6wVPfKWkC0-C'],
    'mimeType': 'application/vnd.google-apps.form'
}
form_file = drive_service.files().create(body=file_metadata).execute()
update = {
    "requests": [{
        "createItem": {
            "item": {
                "title": "Nombre y apellido",
                "questionItem":{
                    "question":{
                        "textQuestion":{
                            "paragraph":False
                        }
                    }
                }
            }, 
            "location": {
                "index": 0
            }
        }
    }]
}
# Update the form with a description
question_setting = forms_service.forms().batchUpdate(
    formId=form_file["id"], body=update).execute()
update2 = {
    "requests": [{
        "deleteItem": {
            "location": {
                "index": 1
            } 
        }
    }]
}

# Update the form with a description
question_setting = forms_service.forms().batchUpdate(
    formId=form_file["id"], body=update2).execute()

# store form id
form_id=open('formid.txt','w')
form_id.write(form_file['id'])
form_id.close()
body='https://docs.google.com/forms/d/'+form_file['id']+'/viewform'

em = EmailMessage()
em["From"] = sender_email
em["To"] = receiver_email
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email,receiver_email,em.as_string())