#!/usr/bin/env python
import os
import json
import boto3

EMAIL_DATA_FILENAME = 'sample_data.json'
EMAIL_TEMPLATE_FILENAME = 'sample_template.html'
CHARSET = "UTF-8"

# AWS Session
session = boto3.session.Session(profile_name='default')
sesClient = session.client('ses')

def getEmailTemplate(senderData, clientData):
    return

def bulkSendEmail(filename=EMAIL_DATA_FILENAME):
    with open(filename) as f:
        data = json.load(f)

        for d in data['clientData']:
            sendEmail(data['senderData'], d)

def getEmailTemplate(senderData, clientData, filename=EMAIL_TEMPLATE_FILENAME):
    with open(filename) as f:
        data = f.read()
        return data.format(
            clientFirstName=clientData['firstName'],
            clientCompanyName=clientData['companyName'],
            clientDateTime=clientData['datetime'],
            senderFirstName=senderData['firstName'],
            phonenumber=senderData['phoneNumber']
        )

def sendEmail(senderData, clientData):
    
    SENDER = "{firstName} {lastName} <{email}>".format(
        firstName=senderData['firstName'],
        lastName=senderData['lastName'],
        email=senderData['email']
    )

    emailTemplate = getEmailTemplate(senderData, clientData)

    sesData = {
        'Source': SENDER,
        'Destination': {
            'ToAddresses': [ clientData['email'] ],
            'BccAddresses': senderData['bccAddresses']
        },
        'Message': {
            'Subject': {
                'Data': senderData['subject'],
                'Charset': CHARSET
            },
            'Body': {
                'Html': {
                    'Data': emailTemplate,
                    'Charset': CHARSET
                }
            }
        }
    }

    print(json.dumps(sesData))
    try:
        response = sesClient.send_email(Source=sesData['Source'], Destination=sesData['Destination'], Message=sesData['Message'])
    except Exception as ex:
        print(ex)

bulkSendEmail()