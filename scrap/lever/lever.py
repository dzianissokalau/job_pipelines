import requests
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import tags
import re





def get_roles(title):
    # software engineer
    swe = True if 'engineer' in title.lower().replace(' ', '') else False
    
    # data scientist
    ds = True if 'datascien' in title.lower().replace(' ', '') \
                            or 'dataanaly' in title.lower().replace(' ', '') \
                            or 'productanaly' in title.lower().replace(' ', '') else False
    
    # data engineer
    de = True if 'dataengineer' in title.lower().replace(' ', '') else False
    
    # engineering manager
    em = True if 'engineeringmanag' in title.lower().replace(' ', '') else False

    # product manager
    pm = True if 'productmanag' in title.lower().replace(' ', '') else False

    # design
    dis = True if 'design' in title.lower().replace(' ', '') else False

    # marketing
    mr =  True if 'marketing' in title.lower().replace(' ', '') else False
    
    roles = {
        'swe': swe,
        'ds': ds,
        'de': de,
        'em': em,
        'pm': pm,
        'dis': dis,
        'mr': mr
    }

    # create dict with roles
    return roles



def get_tags_lists(tags_list, description):
    job_tags = tags.get_list(tags_list, description)
    
    return job_tags    




def get_job_description(job_url):
    # scrap job description
    job_description_url = job_url
    job_description_response = requests.get(job_description_url)
    job_description_html = BeautifulSoup(job_description_response.content, 'html.parser')
    job_description = job_description_html.find_all('div', attrs={'class': 'section page-centered'})
    
    job_description = ''.join([unicodedata.normalize("NFKD", str(d)) for d in job_description])
    
    # unify job description
    job_description = job_description.replace('h5', 'h6')
    job_description = job_description.replace('h4', 'h6')
    job_description = job_description.replace('h3', 'h5')
    job_description = job_description.replace('h2', 'h4')
    job_description = job_description.replace('h1', 'h4')

    return job_description



def get_job_data(raw):
    # create dict to store results
    job_data = dict()
    
    # link to job description + job_id + job name
    job = raw.find('a', attrs={'class': 'posting-title'})
    job_data['job_name'] = job.find(attrs={'data-qa': 'posting-name'}).text
    job_data['job_url'] = job['href']
    job_data['job_id'] = job_data['job_url'].split('/')[-1]
    job_data['job_source'] = 'lever'
    job_data['job_category'] = raw.find('span', class_='sort-by-team posting-category small-category-label department').text
    
    # job roles (filter)
    roles = get_roles(job_data['job_name'])
    for role in roles.keys():
        job_data[role] = roles[role]
    
    
    # job location
    job_data['location'] = raw.find('span', class_='sort-by-location posting-category small-category-label location').text
    job_data['location_simp'] = job_data['location'] if len(job_data['location']) <= 30 else 'Remote'
    
    # job description
    job_data['job_description'] = get_job_description(job_data['job_url']) 
    
    # tags
    job_data['tags'] = get_tags_lists(tags.get_tags(), job_data['job_description']) 
    job_data['tags_short'] = job_data['tags'][0:5] if len(job_data['tags']) >= 5 else job_data['tags']
    
    return job_data



def get_job_id(raw):
    job = raw.find('a', attrs={'class': 'posting-title'})
    job_url = job['href']
    job_id = job_url.split('/')[-1]
    
    return job_id
