from __future__ import print_function

import os.path


import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

#Checks only for emails AFTER this date
#HUGE hit to performance, earlier date = more emails = more processing
DATE = "2023/12/1"

#Some of the general code here was provided by the Gmail API's quick start
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=3001)
        # Save the credentials for the next run
        with open('data/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])


    except HttpError as error:
        print(f'An error occurred: {error}')

    
    #here is the query for finding the messages:
    #you can change around the query to search for a different date
    data = get_messages(service, "'unsubscribe' after:{}".format(DATE))


    messages = clean_messages(service, data)

    complete = []
     
    #Extracting just the links and the names from the messages
    print("final touches...")
    for message in messages:

        message = {
            "name": messages[messages.index(message)][0],
            "link": messages[messages.index(message)][2],
        }

        complete.append(message)

    #dumping all of the messages to json
    print("opening json...")
    f = open("unscriber/unscriber/src/messages.json", "w")
    print("dumping json...")
    f.write(json.dumps(complete))
    f.close()
    print("done!")


      

    


#this function interacts with the API and pulls all emails that match the query
def get_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

#This is the function that finds the unsubscribe link
#If it cannot find a link, or if the link doesn't match the format given, 
#the function will simple return a link to the the email itself, to let the user find the link.
def unmask_message(service, message):
    
    id = message['id']
    result = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
   
    payload = result['payload']
    headers = payload.get("headers")
    values = []
    body = payload.get("body").get("data")
    link = ''


    if body:
        data = base64.urlsafe_b64decode(body)
        clean = data.lower()
        pos = clean.find('>unsubscribe<'.encode())
        pos_start = clean.rfind('href='.encode(), 0, pos) + 5
        pos_end = clean.find('"'.encode(), pos_start,pos) + 1
        link = data[pos_start:pos_end].decode()
    else:
        link = 'https://mail.google.com/mail/?authuser=me@gmail.com#all/' + id


    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")

            if name.lower() == 'from':
                values = [value, id, link]
                return values


#cleans up the raw data from the gmail API into useable information (name of sender + unsubscribe link)
def clean_messages(service, list):
    
    total = len(list)
    items = []
    print("found {} messages\nprocessing....".format(total))
    for x in range(total):

        data = unmask_message(service, list[x])

        split_data = data[0].rsplit("<")
        cleaned_data = split_data[0].strip('" ')

        #Incredibly inefficient, I will look into updating it
        #If a sender is found twice, don't add it
        if not linear_search(items, [cleaned_data,]): 
            items.append([cleaned_data, data[1], data[2]])

    return items

#Simple linear search     
def linear_search(array, item):
    for x in array:
        if x[0].lower() == item[0].lower():
            return True

    return False


       

        


if __name__ == '__main__':
    main()

