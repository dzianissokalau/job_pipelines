import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import json
import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import greenhouse

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
    'opentable': 'OpenTable',
    'gusto': 'gusto',
    'gomotive': 'Motive',
    'pleo': 'pleo',
    'alpaca': 'Alpaca',
    'grammarly': 'Grammarly',
    'quora': 'Quora',
    'goclio': 'Clio',
    'anaconda': 'Anaconda',
    'digit': 'Digit',
    'canonical': 'Canonical',
    'narvar': 'Narvar',
    'leagueinc': 'League',
    'fivetran': 'Fivetran',
    'dataikujobs': 'Dataiku',
    'reddit': 'Reddit'
}


new_listings = []

url_base = 'https://boards.greenhouse.io'
for company in companies.keys():
    company_url = url_base + '/' + company
    response = requests.get(company_url)
    time.sleep(5)
    
    response_html = BeautifulSoup(response.content, 'html.parser')
    
    #company name
    company_name = companies[company]
    print(company_name)
    
    # openings
    results = response_html.find_all('div', class_='opening')
    for result in results:
        job_id = result.find('a')['href'].split('/')[-1]
        new_listings.append(job_id)
        if job_id not in listings.keys():
            print(f'new listing: {job_id}')

            job_data = greenhouse.get_job_data(result)            

            # additional data
            job_data['company_name'] = company_name
            job_data['img_url'] = 'https://storage.googleapis.com/findremote/' + company_name.lower() + '.jpg'
            job_data['status'] = 'active'
            
            # add timestamp if job is not in db yet
            job_data['datetime'] = pd.to_datetime(datetime.datetime.utcnow())
            job_data['unix_timestamp'] = int((job_data['datetime'].replace(tzinfo=None) - datetime.datetime(1970, 1, 1)).total_seconds())        

            # write to Fire Store (Content)
            doc_ref = db.collection(u'new_listings').document(job_data['job_id'])
            doc_ref.set(job_data)
            
            time.sleep(5)



# if past listings not in new listings set status "archived" 
for listing in listings.keys():
    if listing not in new_listings:
        job_data = listings[listing]
        job_data['status'] = 'archived'
        # write to Fire Store (Content)
        doc_ref = db.collection(u'new_listings').document(job_data['job_id'])
        doc_ref.set(job_data)

