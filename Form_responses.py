from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from datetime import date, timedelta
from email.message import EmailMessage
import smtplib
import ssl
import json
import string

hoy=date.today()
manana= hoy + timedelta(1)
fecha=str(manana).split('-')
fecha_nueva=str(fecha[2])+'/'+str(fecha[1])


# Load the saved credentials from the token file
with open('token.json', 'r') as token:
    credentials = Credentials.from_authorized_user_info(info=json.load(token))

# Set up the Forms APIs
forms_service = build('forms', 'v1', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

formid=open('formid.txt','r')
for line in formid:
    id=line

# Gets results
try:
    results = forms_service.forms().responses().list(formId=id).execute()
    responses=dict()
    for result in results['responses']:
        responses[str(result['createTime'])]=list(result['answers'].values())[0]['textAnswers']['answers'][0]['value']
    orden=list(responses.keys())
    orden.sort()

    texto=''
# Creates whatsapp list
    i=1
    aforo=24
    for item in orden:
        if i==1:
            texto+='Lista cancha -3 \t4:15\n' + fecha_nueva + '\n'
        if i==aforo+1:
            texto+='\n\nLista de espera:'
        if i>aforo:
            texto+='\n'+str(i-aforo)+'. '+responses[item]
            i+=1
            continue
        texto+='\n'+str(i)+'. '+responses[item]     
        i+=1
except:
    texto='No results'

# email details
sender_email = 'seba123612@gmail.com'
sender_password = 'kkaupfbklzumzfgs'
receiver_email = 'seba123612@gmail.com'
subject = 'Lista grupo organizado'
body = texto

em = EmailMessage()
em["From"] = sender_email
em["To"] = receiver_email
em["Subject"] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email,receiver_email,em.as_string())


