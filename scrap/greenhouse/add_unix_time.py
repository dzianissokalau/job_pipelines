import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import greenhouse


#initializing firestore
cert_path = '/Users/dzianis/github/' + 'findremote-firebase-adminsdk-p9cw7-633a39d4a9.json'
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)

# connect to db
db = firestore.client()


# get data from FireStore
listings_db = db.collection(u'listings').stream()

listings = dict()
for listing in listings_db:
    listings[listing.id] = listing.to_dict()



# add unix time 
for listing in listings.keys():
    job_data = listings[listing]

    if 'datetime' in list(job_data.keys()):
        job_datetime = job_data['datetime']
        if type(job_datetime) == str:
            job_data['unix_timestamp'] = int((datetime.datetime.strptime(job_datetime, "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime(1970, 1, 1)).total_seconds())
        else:
            job_data['unix_timestamp'] = int((job_datetime.replace(tzinfo=None) - datetime.datetime(1970, 1, 1)).total_seconds())
        # write to Fire Store (Content)
        doc_ref = db.collection(u'listings').document(job_data['job_id'])
        doc_ref.set(job_data) 
    else:
        print(f'{listing} doesnt have datetime, current status: {job_data["status"]}')



