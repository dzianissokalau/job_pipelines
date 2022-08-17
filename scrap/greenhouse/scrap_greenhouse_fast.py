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
cert_path = '/home/densokolov88/github/' + 'findremote-firebase-adminsdk-p9cw7-633a39d4a9.json'
cred = credentials.Certificate(cert_path)
firebase_admin.initialize_app(cred)

# connect to db
db = firestore.client()




# get data from FireStore
listings_db = db.collection(u'listings').stream()

listings = dict()
for listing in listings_db:
    listings[listing.id] = listing.to_dict()
    
    

    
companies = {
    'github': 'GitHub', 
    'gitlab': 'GitLab', 
    'invision': 'InVision', 
    'blockchain': 'Blockchain', 
    'automatticcareers': 'Automattic', 
    'monzo': 'Monzo', 
    'mozilla': 'Mozilla', 
    'autoscout24': 'Autoscout24',
    'zapiercareers': 'Zapier' 
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
    
    # openings
    results = response_html.find_all('div', class_='opening')
    for result in results:
        job_id = greenhouse.get_job_id(result)
        new_listings.append(job_id)
        

print('lenght of new listings: ', len(new_listings))
print('lenght of listings: ', len(listings.keys()))


# if past listings not in new listings set status "archived" 
for lising in listings.keys():
    if listing not in new_listings:
        print('archived: ', listing, url_base+job_data['job_url'])
        job_data = db.collection(u'listings').document(listing).get().to_dict()
        job_data['status'] = 'archived'
        # write to Fire Store (Content)
        doc_ref = db.collection(u'listings').document(job_data['job_id'])
        doc_ref.set(job_data)        
