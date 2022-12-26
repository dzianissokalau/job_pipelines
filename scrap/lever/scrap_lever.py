import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import unicodedata
import json
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import lever

import tags
import re



#initializing firestore
cert_path = '/home/densokolov88/github/' + 'findremote-firebase-adminsdk-p9cw7-633a39d4a9.json'
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)

# connect to db
db = firestore.client()


# get data from FireStore
listings_db = db.collection(u'new_listings').where('status', '==', 'active').stream()

listings = dict()
for listing in listings_db:
    listings[listing.id] = listing.to_dict()    
    

    
companies = {
    'stackadapt': 'StackAdapt',
    'benchsci': 'BenchSci',
    'koho': 'KOHO',
    'spotify': 'Spotify',
    'binance': 'Binance',
    'kraken': 'Kraken',
    'lime': 'Lime',
    'gantry': 'Gantry',
    'dbtlabs': 'dbt Labs',
    'clearbit': 'Clearbit',
    'sonatype': 'Sonatype',
    'gettyimages': 'gettyimages',
    'scribd': 'Scribd',
    'canva': 'Canva',
    'xero': 'Xero'
}


new_listings = []

url_base = 'https://jobs.lever.co'
for company in companies.keys():
    print(company)
    company_url = url_base + '/' + company
    response = requests.get(company_url)
    time.sleep(5)
    
    response_html = BeautifulSoup(response.content, 'html.parser')
    
    #company name
    company_name = companies[company]
    
    # openings
    results = response_html.find_all('div', class_='posting')
    for result in results:
        job_data = lever.get_job_data(result)
        new_listings.append(job_data['job_id'])

        # additional data
        job_data['company_name'] = company_name
        job_data['img_url'] = 'https://storage.googleapis.com/findremote/' + company_name.lower() + '.jpg'
        job_data['status'] = 'active'


        # add timestamp if job is not in db yet
        if job_data['job_id'] not in listings.keys() or 'datetime' not in listings[job_data['job_id']].keys():
            job_data['datetime'] = pd.to_datetime(datetime.datetime.utcnow())
        else:
            job_data['datetime'] = listings[job_data['job_id']]['datetime']  

        if type(job_data['datetime']) == str:
            job_data['unix_timestamp'] = int((datetime.datetime.strptime(job_data['datetime'], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime(1970, 1, 1)).total_seconds())
        else:
            job_data['unix_timestamp'] = int((job_data['datetime'].replace(tzinfo=None) - datetime.datetime(1970, 1, 1)).total_seconds())      

        # write to Fire Store (Content)
        doc_ref = db.collection(u'new_listings').document(job_data['job_id'])
        doc_ref.set(job_data)


        time.sleep(5)


# if past listings not in new listings set status "archived" 
for listing in listings.keys():
    if listing not in new_listings:
        job_data = db.collection(u'listings').document(listing).get().to_dict()
        job_data['status'] = 'archived'
        # write to Fire Store (Content)
        doc_ref = db.collection(u'listings').document(job_data['job_id'])
        doc_ref.set(job_data)  
