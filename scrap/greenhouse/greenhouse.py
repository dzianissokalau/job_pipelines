import requests
from bs4 import BeautifulSoup
import pandas as pd





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



def get_tags(description):
    # tags
    tags_list = ['javascript',	'python',	'java',	'c#',	'php',	'android',	'html',	'jquery',	'c++',	'css',	'mysql',	'sql',	'nodejs',	'reactjs',	'asp.net',	'json',	'.net',	'sql-server',	'swift',	'django',	'objective-c',	'angular',	'pandas',	'regex',	'ruby',	'ajax',	'linux',	'xml',	'vba',	'spring',	'typescript',	'database',	'wordpress',	'wpf',	'mongodb',	'windows',	'postgresql',	'xcode',	'bash',	'oracle',	'git',	'aws',	'vb.net',	'multithreading',	'flutter',	'firebase',	'dataframe',	'eclipse',	'azure',	'react-native',	'docker',	'algorithm',	'visual-studio',	'scala',	'powershell',	'numpy',	'api',	'selenium',	'performance',	'winforms',	'vuejs',	'matlab',	'sqlite',	'shell',	'express',	'android-studio',	'csv',	'linq',	'maven',	'unit-testing',	'swing',	'tensorflow',	'kotlin',	'spark',	'dart',	'symfony',	'tsql',	'codeigniter',	'opencv',	'perl',	'unity3d',	'matplotlib',	'sockets',	'golang',	'cordova',	'xaml',	'oop',	'ubuntu',	'ms-access',	'parsing',	'elasticsearch',	'security',	'jsp',	'github',	'nginx',	'flask',	'machine-learning',	'delphi',	'kubernetes',	'haskell',	'xamarin',	'ssl',	'ggplot2',	'jenkins',	'gradle',	'visual-studio-code',	'google-apps-script',	'testing',	'tkinter',	'unix',	'google-app-engine',	's3',	'google-sheets',	'web-scraping',	'hadoop',	'mongo',	'heroku',	'animation',	'curl',	'math',	'actionscript',	'assembly',	'image-processing',	'keras',	'gcp',	'd3.js',	'magento',	'networking',	'javafx',	'optimization',	'google-cloud-firestore',	'facebook-graph-api',	'cocoa-touch',	'amazon-ec2',	'pyspark',	'xamarin.forms',	'jdbc',	'data-structures',	'dplyr',	'cakephp',	'awk',	'design-patterns',	'visual-c++',	'rust',	'beautifulsoup',	'ssh',	'kafka',	'sharepoint',	'bootstrap',	'vim',	'graph',	'silverlight',	'plsql',	'aws-lambda',	'scikit-learn',	'websocket',	'shiny',	'sass',	'vuejs2',	'deep-learning',	'extjs',	'apache-flex']

    base = description.lower().replace('-', '').replace(' ', '')
    
    tags = []
    for tag in tags_list:
        if tag.lower().replace('-', '').replace(' ', '') in base:
            tags.append(tag)
    
    return tags    





def get_job_description(job_url):
    # scrap job description
    job_description_url = job_url
    job_description_response = requests.get(job_description_url)
    job_description_html = BeautifulSoup(job_description_response.content, 'html.parser')
    job_description = str(job_description_html.find('div', id='content'))
    
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
    job = raw.find('a')
    job_data['job_name'] = job.text
    job_data['job_url'] = 'https://boards.greenhouse.io' + job['href']
    job_data['job_id'] = job_data['job_url'].split('/')[-1]
    
    # job roles (filter)
    roles = get_roles(job_data['job_name'])
    for role in roles.keys():
        job_data[role] = roles[role]
    
    
    # job location
    job_data['location'] = raw.find('span', class_='location').text
    job_data['location_simp'] = job_data['location'] if len(job_data['location']) <= 30 else 'Remote'
    
    # job description
    job_data['job_description'] = get_job_description(job_data['job_url']) 
    
    # tags
    job_data['tags'] = get_tags(job_data['job_description'])
    job_data['tags_short'] = job_data['tags'][0:5] if len(job_data['tags']) >= 5 else job_data['tags']
    
    return job_data



def get_job_id(raw):
    job = raw.find('a')
    job_url = job['href']
    job_id = job_url.split('/')[-1]
    
    return job_id