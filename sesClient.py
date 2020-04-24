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

def bulkSendEmail(filename=EMAIL_DATA_FILENAME):
    with open(filename) as f:
        data = json.load(f)

        clientIndex = 0
        for d in data['clientData']:
            sendEmail(data, clientIndex)
            clientIndex += 1

def getEmailTemplate(htmlData, senderData, clientData, filename=EMAIL_TEMPLATE_FILENAME):

    def get(param):
        source, key = param.split('.')
        if source == 'senderData':
            return senderData[key]
        elif source == 'clientData':
            return clientData[key]

    paramsData = {k:get(v) for k, v in htmlData.items()}
    
    with open(filename) as f:
        data = f.read()
        return data.format(**paramsData)

def sendEmail(data, clientIndex):
    senderData = data['senderData']
    clientData = data['clientData'][clientIndex]
    
    SENDER = "{firstName} {lastName} <{email}>".format(
        firstName=senderData['firstName'],
        lastName=senderData['lastName'],
        email=senderData['email']
    )

    emailTemplate = getEmailTemplate(data['htmlData'], senderData, clientData)

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

    try:
        response = sesClient.send_email(Source=sesData['Source'], Destination=sesData['Destination'], Message=sesData['Message'])
    except Exception as ex:
        print(ex)

# Execution

bulkSendEmail()