import re




def search_tag(word, text):
    """
    Check if a word is in a text.

    Parameters
    ----------
    word : str
    text : str
    """
    pattern = r'(^|[^\w]){}([^\w]|$)'.format(word)
    pattern = re.compile(pattern, re.IGNORECASE)
    matches = re.search(pattern, text)
    
    return bool(matches)



def get_list(tags, text):
    tags_list = []
    
    for tag in tags:
        if '++' in tag:
            new_tag = tag.replace('++', 'plusplus')
            new_text = text.replace('++', 'plusplus')
            if search_tag(new_tag, new_text):
                tags_list.append(tag)
        elif search_tag(tag, text):
            tags_list.append(tag)
    
    return tags_list



def get_tags():
    return [
            'javascript',
            'python',
            'java',
            'c#',
            'php',
            'android',
            'html',
            'jquery',
            'c++',
            'css',
            'mysql',
            'sql',
            'nodejs',
            'reactjs',
            'asp.net',
            'json',
            '.net',
            'sql-server',
            'swift',
            'django',
            'objective-c',
            'angular',
            'excel',
            'pandas',
            'regex',
            'ruby',
            'ajax',
            'linux',
            'xml',
            'vba',
            'spring',
            'typescript',
            'database',
            'wordpress',
            'wpf',
            'mongodb',
            'windows',
            'postgresql',
            'xcode',
            'bash',
            'oracle',
            'git',
            'aws',
            'vb.net',
            'multithreading',
            'flutter',
            'firebase',
            'dataframe',
            'eclipse',
            'azure',
            'react-native',
            'docker',
            'algorithm',
            'visual-studio',
            'scala',
            'powershell',
            'numpy',
            'api',
            'selenium',
            'winforms',
            'vuejs',
            'matlab',
            'sqlite',
            'loops',
            'rest',
            'shell',
            'express',
            'android-studio',
            'csv',
            'linq',
            'maven',
            'unit-testing',
            'swing',
            'tensorflow',
            'kotlin',
            'spark',
            'dart',
            'symfony',
            'tsql',
            'codeigniter',
            'opencv',
            'perl',
            'unity3d',
            'matplotlib',
            'sockets',
            'golang',
            'cordova',
            'xaml',
            'oop',
            'ubuntu',
            'ms-access',
            'parsing',
            'elasticsearch',
            'security',
            'jsp',
            'github',
            'nginx',
            'flask',
            'machine-learning',
            'delphi',
            'kubernetes',
            'haskell',
            'xamarin',
            'ssl',
            'ggplot2',
            'jenkins',
            'gradle',
            'visual-studio-code',
            'google-apps-script',
            'testing',
            'tkinter',
            'unix',
            'google-app-engine',
            's3',
            'google-sheets',
            'web-scraping',
            'hadoop',
            'mongo',
            'heroku',
            'animation',
            'curl',
            'math',
            'actionscript',
            'assembly',
            'image-processing',
            'keras',
            'gcp',
            'd3.js',
            'magento',
            'networking',
            'javafx',
            'optimization',
            'google-cloud-firestore',
            'facebook-graph-api',
            'cocoa-touch',
            'amazon-ec2',
            'pyspark',
            'xamarin.forms',
            'jdbc',
            'data-structures',
            'dplyr',
            'cakephp',
            'awk',
            'design-patterns',
            'visual-c',
            'rust',
            'beautifulsoup',
            'ssh',
            'kafka',
            'sharepoint',
            'bootstrap',
            'vim',
            'graph',
            'silverlight',
            'plsql',
            'aws-lambda',
            'scikit-learn',
            'websocket',
            'shiny',
            'sass',
            'vuejs2',
            'deep-learning',
            'extjs',
            'apache-flex'
        ]