# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:52:03 2018

@author: Peng Wang

Tokenize text, extract keywords, and recommend jobs by matching keywords from resume with jobs
"""

import re
from nltk.corpus import stopwords
from collections import Counter 
import pandas as pd
import PyPDF2
import config
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# The following data science skill sets are modified from 
# https://github.com/yuanyuanshi/Data_Skills/blob/master/data_skills_1.py
data_science_skills=['Python','pandas', 'numpy', 'scipy','Sql','Cluster Analysis', 'Word Embedding','LDA', 'NMF', 'PCA','Neural Nets',
'Mysql', 'SqlServer', 'Cassandra', 'Hbase', 'ElasticSearch D3.js', 'DC.js', 'Plotly, kibana','ggplot','HTML', 'CSS', 'Angular 6', 'Logstash', 'Kafka', 'Git','Open CV','Deep learning']
program_languages = ['bash','r','python','java','c++','ruby','perl','matlab','javascript','scala','php']
analysis_software = ['excel','tableau','sas','spss','d3','saas','pandas','numpy','scipy','sps','spotfire','scikit','splunk','power','h2o']
ml_framework = ['pytorch','tensorflow','caffe','caffe2','cntk','mxnet','paddle','keras','bigdl']
bigdata_tool = ['hadoop','mapreduce','spark','pig','hive','shark','oozie','zookeeper','flume','mahout','etl']
ml_platform = ['aws','azure','google','ibm']
methodology = ['agile','devops','scrum']
databases = ['sql','nosql','hbase','cassandra','mongodb','mysql','mssql','postgresql','oracle','rdbms','bigquery']
network_skills=['Firewalls','Switches','Troubleshooting','Innovation','Cybersecurity','Collaboration','Hardware','Network Security',
                'Linux','VPN','Protocols','Routers','SIEM','IDS','Access control','Windows','Encryption solutions','Coding',
                'Hardware','Threat modeling','Vulnerability testing','LAN', 'WAN']+['Network Architecture','Network Design','Border Gateway Protocol','BGP','Multiprotocol Label Switching','MPLS',
                             'Wide Area Network (WAN)','Cisco Systems Products','Networking','Data Center','Routing','Network Security',
                             'Firewalls','Internet Protocol','IP','Switches','Voice over IP','VoIP','Virtual Private Network','VPN',
                             'Internet Protocol Suite','TCP/IP','Telecommunications','Routers','Juniper Networks Products','Integration',
                             'Quality of Service','QoS','SD-WAN','Software Defined Networking','Cisco Nexus','Switching','Open Shortest Path First','OSPF',
                             'Network Engineering','Fortinet','LAN-WAN','Disaster Recovery','Cisco ASA','Implementing','troubleshooting',
                            'network security solutions','Planning' ,'multi vendor firewalls','Cisco ASA', 'Checkpoint',
                            'Juniper/Netscreen', 'Fortinet', 'FWSM','Zenoss', 'Solarwinds', 'Cisco Prime','multi client data center',
                            'Firewall', 'IOS','F5 load balancers', 'SSL certificate updates', 'I-Rule','Configuration of Cisco Routers',                            'Nexus','Bluecoat Proxy','ITIL process']

#program_languages + analysis_software + ml_framework + bigdata_tool + databases + ml_platform + methodology+data_science_skills
ItSkills= ['bash','r','python','java','c++','ruby','perl','matlab','javascript','scala','php','excel','tableau','sas','spss','d3','saas','pandas','numpy','scipy','sps','spotfire','scikit','splunk','power','h2o','pytorch','tensorflow','caffe','caffe2','cntk','mxnet','paddle','keras','bigdl','hadoop','mapreduce','spark','pig','hive','shark','oozie','zookeeper','flume','mahout','etl','aws','azure','google','ibm','agile','devops','scrum','sql','nosql','hbase','cassandra','mongodb','mysql','mssql','postgresql','oracle','rdbms','bigquery','Salesforce','Business Analyst','UI Developer','Big Data','Etl', 'Informatica', 'Ios', 'Quality Analyst','MySQL', 'PostgreSQL', 'Oracle', 'RDBMS', 'dBASE', 'Clipper',
       'FoxPro', 'Firebase', 'Mongodb', 'Java', 'J2EE', 'Oracle Fusion','Oracle Cloud', 'Salesforce', 'Devops Android','Business Analyst', 'UI Developer', 'DBAs',
       'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Big Data', 'Tableau', 'Networking','DBAs', 'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Tableau',
       'J2EE','Devops Android', 'UI Developer', 'DBAs', 'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Tableau', 'Data Science', 'Python', 'Machine Learning', 'SAS',
       'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis', 'Ssrs, Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas',
       'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'DataMining', 'Text Mining', 'Oops', 'Deep Learning',
       'Web Analytics', 'Time Series', 'Regression', 'Tensorflow', 'Azure', 'Linear Regression', 'Logistic Regression', 'Decision Tree', 'Random Forest', 'Data Structure',
       'Computer Vision', 'Data Science', 'Python', 'Machine Learning', 'SAS', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis',
       'Ssrs', 'Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling', 'Regression',
       'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression', 'Tensorflow', 'Azure', 'Linear Regression',
       'Logistic Regression', 'Decision Tree', 'Random Forest', 'Data Science', 'Python', 'Machine Learning', 'SAS', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming',
       'SQL server reporting', 'Msbi Ssis', 'Ssrs', 'Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce',
       'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression',
       'Tensorflow', 'Azure', 'Linear Regression', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis', 'Ssrs', 'Msbi',
       'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling, Regression', 'Patterns',
       'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression','Tensorflow', 'Azure', 'Linear Regression', 'Java', 'Scala',
       'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce',
       'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series',
       'Regression', 'Tensorflow', 'Azure', 'Linear Regression', 'IHS', 'WAS', 'Java EE', 'SQL Server', '.NET core', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api',
       'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', '.NET core', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api', 'Mvc', 'Javascript',
       'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api', 'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL',
       'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Web Api', 'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Web Api', 'Mvc',
       'Javascript', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii', 'FuelPHP', 'React', 'Vue', 'Angular', 'Ember', 'Backbone', 'PHP', 'Laravel',
       'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii', 'FuelPHP', 'React', 'Vue', 'Angular', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon',
       'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon',
       'FuelPHP','React', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii, FuelPHP', 'React', 'Vue', 'Angular', 'PHP', 'Laravel', 'CodeIgniter',
       'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter',
       'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React','Creo 4.0','Catia V5','UGNX 11.0','SolidWorks 2017','Microstation','AutoCAD 10','Altium Designer 17','RSD','Mentor Capital Logic','Harness XL','Windchill 10.2','Teamcenter','Projectwise','Intralink','Pro/PDM','Confidential','Minitab','PLM','Ansys v16.0','SimWise 4D','FEMAP v11.4.0','LabVIEW','Matlab 2016b','Maple 2016','MS Office 2016','One Note','Visio','Project','Publisher','Adobe Creative Suite','tower Structural Analysis','Weight Differentials','Tension Analysis' ,'OSP Design','GIS Analyst','ArcGIS','OSP Best Route','Quality Control','Yuma software','Aerial Fiber','Underground Fiber','Buried Fiber','AutoCAD','ETS','Make Ready Engineering','Pole Analyst','CATIA V5','CATIA V4','Pro/E','AutoCAD','ENOVIA (LCA)','VELOCITY','REDARS','PDM','EIDS','BOM','IVT','ENCAPTA','POWERPOINT','TEAMCENTER','GD &T','3D (Model Based Definition)','SmartTeam (PLM)','MS Suite','CATIA V5','UGNX','Pro – E','Solid works','Ennovia','AngularJS','NodeJS','HTML5', 'CSS','AWS', 'ReST','SOAP','Spring framework','selenium automation']
bankingskills=['P&L','Internal Audit','Cashing','Inventory Movement', 'Business Analyst', 'Accounting', 'Capital Markets', 'Corporate Actions','Investment Banking', 'project manager', 'GAAP','IFRS','Leadership','Supervision', 'Team Building', 'Time Management', 'Management', 'Problem Solving', 'Critical Problem Analysis', 'Accounting principle', 'Financial Reporting', 'Presentation', 'Investment analysis', 'Stock','Currency trading', 'VBA','SAP', 'SPSS', 'MEGASTAT', 'QuickBooks Pro', 'MS Project', 'Erwin', 'Regression','Six Sigma', 'Quality center','General accounting','bookkeeping','Data entry','Auditing','Inventory','VendMax', 'analytical','customer service','financial planning','analysis', 'project management', 'GAAP', 'DCAA', 'FAR','CAS', 'SOX', 'OMB Circular','testing', 'reporting','SAP', 'FICO','HANA' ,'Asset', 'Treasury', 'Risk','Cash','Business','Warehouse','Managerial', 'Tax', 'GAAP','cost','strategic', 'finance', 'program management', 'supply chain','fiscal platforms','businesses models','Adjunct', 'Accounting instructor', 'Business Development', 'Mentoring', 'Management Accounting','Merger','Acquisition', 'Sales Compensation', 'Supply Chain Management', 'GAAP', 'Sarbanes-Oxley', 'JD Edwards', 'Microsoft Dynamics 365', 'Business Objects', 'Live Link', 'Essbase', 'MFG Pro', 'QuickBooks', 'Star Office', 'Visio', 'JDE ERP8', 'Hyperion', 'Clarity', 'Cognos', 'Oracle Discoverer', 'SmartView','Mass 500', 'MAS', 'ACCPAC', 'Peachtree', 'SAP', 'ERP', 'XERO', 'Open Systems','TurboTaxCommunity']
healthskills=['Medical billing','Triage','Anatomy','MediSoft','Health records','medical records','Medical terminology','Patient scheduling','Treatment','Treatment plan development','Crisis intervention','Therapeutic','In home therapy','Psychoeducation','HIPAA','compliance','EMR','operating room', 'Surgical nurse','laser','theatre nurse','Vital Signs','Phlebotomy','Medical History','Administrative','Patient Care','Electrocardiogram','EHR','EPM', 'Insurance Billing', 'Patient Assessment', 'Appointment Scheduling', 'Injections', 'TB']
ItSkills=list(set(ItSkills))
bankingskills=list(set(bankingskills))
education = ['master','phd','undergraduate','bachelor','mba','IT','Finance','Accounting']
overall_skills_dict = list(set(network_skills))+ItSkills
#overall_skills_dict = data_science_skills
overall_dict=overall_skills_dict+education

#overall_dict=list(set(overall_dict))
'''other=['Salesforce','Business Analyst','UI Developer','Big Data','Etl', 'Informatica', 'Ios', 'Quality Analyst','MySQL', 'PostgreSQL', 'Oracle', 'RDBMS', 'dBASE', 'Clipper',
       'FoxPro', 'Firebase', 'Mongodb', 'Java', 'J2EE', 'Oracle Fusion','Oracle Cloud', 'Salesforce', 'Devops Android','Business Analyst', 'UI Developer', 'DBAs',
       'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Big Data', 'Tableau', 'Networking','DBAs', 'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Tableau',
       'J2EE','Devops Android', 'UI Developer', 'DBAs', 'Embedded Systems', '.NET', 'Hadoop', 'SQL Developer', 'Tableau', 'Data Science', 'Python', 'Machine Learning', 'SAS',
       'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis', 'Ssrs, Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas',
       'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'DataMining', 'Text Mining', 'Oops', 'Deep Learning',
       'Web Analytics', 'Time Series', 'Regression', 'Tensorflow', 'Azure', 'Linear Regression', 'Logistic Regression', 'Decision Tree', 'Random Forest', 'Data Structure',
       'Computer Vision', 'Data Science', 'Python', 'Machine Learning', 'SAS', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis',
       'Ssrs', 'Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling', 'Regression',
       'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression', 'Tensorflow', 'Azure', 'Linear Regression',
       'Logistic Regression', 'Decision Tree', 'Random Forest', 'Data Science', 'Python', 'Machine Learning', 'SAS', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming',
       'SQL server reporting', 'Msbi Ssis', 'Ssrs', 'Msbi', 'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce',
       'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression',
       'Tensorflow', 'Azure', 'Linear Regression', 'Java', 'Scala', 'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Msbi Ssis', 'Ssrs', 'Msbi',
       'Sql Reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce', 'Parametric Design', 'Modeling, Regression', 'Patterns',
       'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series', 'Regression','Tensorflow', 'Azure', 'Linear Regression', 'Java', 'Scala',
       'Hadoop', 'Hive', 'Bigdata', 'Programming', 'SQL server reporting', 'Artificial Intelligence', 'Pandas', 'Pyspark', 'Sklearn', 'Flask', 'Django', 'Map Reduce',
       'Parametric Design', 'Modeling', 'Regression', 'Patterns', 'Data Mining', 'Text Mining', 'Oops', 'Deep Learning', 'Web Analytics', 'Time Series',
       'Regression', 'Tensorflow', 'Azure', 'Linear Regression', 'IHS', 'WAS', 'Java EE', 'SQL Server', '.NET core', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api',
       'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', '.NET core', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api', 'Mvc', 'Javascript',
       'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Rdlc', 'Linq', 'Sql', 'Web Api', 'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL',
       'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Web Api', 'Mvc', 'Javascript', 'Web Services', 'Oracle', 'MS SQL', 'Java EE', 'SQL Server', 'C#', 'ASP.NET', 'Web Api', 'Mvc',
       'Javascript', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii', 'FuelPHP', 'React', 'Vue', 'Angular', 'Ember', 'Backbone', 'PHP', 'Laravel',
       'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii', 'FuelPHP', 'React', 'Vue', 'Angular', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon',
       'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon',
       'FuelPHP','React', 'PHP', 'Laravel', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'CakePHP', 'Yii, FuelPHP', 'React', 'Vue', 'Angular', 'PHP', 'Laravel', 'CodeIgniter',
       'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter', 'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React', 'Vue', 'Angular', 'CodeIgniter',
       'Symfony', 'Zend', 'Phalcon', 'FuelPHP', 'React']
Design=['Creo 4.0','Catia V5','UGNX 11.0','SolidWorks 2017','Microstation','AutoCAD 10','Altium Designer 17','RSD','Mentor Capital Logic','Harness XL','Windchill 10.2','Teamcenter','Projectwise','Intralink','Pro/PDM','Confidential','Minitab','PLM','Ansys v16.0','SimWise 4D','FEMAP v11.4.0','LabVIEW','Matlab 2016b','Maple 2016',
'MS Office 2016','One Note','Visio','Project','Publisher','Adobe Creative Suite','tower Structural Analysis','Weight Differentials','Tension Analysis' ,'OSP Design','GIS Analyst','ArcGIS','OSP Best Route','Quality Control','Yuma software','Aerial Fiber','Underground Fiber','Buried Fiber','AutoCAD','ETS','Make Ready Engineering','Pole Analyst','CATIA V5','CATIA V4','Pro/E','AutoCAD','ENOVIA (LCA)','VELOCITY','REDARS','PDM','EIDS','BOM','IVT','ENCAPTA','POWERPOINT','TEAMCENTER','GD &T','3D (Model Based Definition)','SmartTeam (PLM)','MS Suite','CATIA V5','UGNX','Pro – E','Solid works','Ennovia','AngularJS','NodeJS','HTML5', 'CSS','AWS', 'ReST','SOAP','Spring framework','selenium automation']
#other=list(set(other))
Design=list(set(Design))
overall_skills_dict_data_analyst=['Data Analysis','Data Visualization','Data Analytics','Python','Statistical Data Analysis','IBM SPSS','MySQL','Google Data Studio','Data Science','Google BigQuery',
                     'Machine Learning','Databases','Data Modeling','Big Data','Visual Basic for Applications','VBA','Big Data Analytics',
                     'Business Intelligence Tools','Data Warehousing','Latent Class Analysis','Tableau','SQL','R','Microsoft Access',
                     'Statistics','Data Mining','Microsoft Power BI','Analytics','Google Analytics','Microsoft SQL Server',
                     'SAS','Extract', 'Transform', 'Load' ,'ETL','Business Analysis','Business Intelligence','BI','SAS Programming',
                     'QlikView','Hive','Statistical Modeling']
overall_skills_dict_full_stack_developer=['AngularJS','JavaScript','Node.js','Cascading Style Sheets','CSS','Web Development',
                                          'MySQL','jQuery','Full-Stack Development','HTML5','Git','AJAX','Laravel','Back-End Web Development',
                                          'HTML','PHP','Front-end Development','React.js','Python','Bootstrap','SQL','TypeScript',
                                          'MongoDB','Amazon Web Services','AWS','Software Development','Docker Products','Java',
                                          'Vue.js','PostgreSQL','Symfony','Microservices','GitHub','CodeIgniter','React Native','C#',
                                          'SASS','Express.js','Redux.js','Spring Boot','Scrum','Django']
overall_skills_dict_IT_consultant=['SQL','IT Consulting','Java','Consulting','Linux','Oracle Database','JavaScript','Software Development',
                                   'Software Project Management','Project Management','MySQL','Scrum','Business Intelligence','BI',
                                   'Information Technology','Microsoft SQL Server','Agile Methodologies','Integration','ITIL',
                                   'HTML','Active Directory','Windows Server','Windows','IT Service Management','XML',
                                   'Virtualization','Networking','Microsoft Exchange','AngularJS','VMware','Office 365','Requirements Analysis',
                                   'Business Analysis','Cloud Computing','Microsoft Azure','System Administration','Databases','Unix','CSS',
                                   'PHP','Technical Support','IT Management','Microsoft Access','Software Development Life Cycle','SDLC',
                                   'PL/SQL','IT Strategy','Solution Architecture','Web Development','Programming','C#','jQuery','Eclipse',
                                   'Jira','Change Management','Unified Modeling Language','UML','.NET Framework','Oracle SQL Developer',
                                   'Git','ASP.NET MVC','PRINCE2','Vendor Management','Network Administration','Servers','React.js','Node.js',
                                   'Python','IT Operations','Enterprise Architecture','Windows 10','Troubleshooting','Operating Systems','COBIT']
overall_skills_dict_network=['Network Architecture','Network Design','Border Gateway Protocol','BGP','Multiprotocol Label Switching','MPLS',
                             'Wide Area Network (WAN)','Cisco Systems Products','Networking','Data Center','Routing','Network Security',
                             'Firewalls','Internet Protocol','IP','Switches','Voice over IP','VoIP','Virtual Private Network','VPN',
                             'Internet Protocol Suite','TCP/IP','Telecommunications','Routers','Juniper Networks Products','Integration',
                             'Quality of Service','QoS','SD-WAN','Software Defined Networking','Cisco Nexus','Switching','Open Shortest Path First','OSPF',
                             'Network Engineering','Fortinet','LAN-WAN','Disaster Recovery','Cisco ASA']
overall_skills_dict= overall_skills_dict_data_analyst +overall_skills_dict_IT_consultant+overall_skills_dict_full_stack_developer+overall_skills_dict_network+Design
#overall_skills_dict = program_languages + analysis_software + ml_framework + bigdata_tool + databases + ml_platform + methodology+other+Design
overall_dict=overall_skills_dict+education'''
jobs_info_df = pd.DataFrame()


def Jaccard_Similarity(doc1, doc2):
    # List the unique words in a document
    words_doc1 = set(doc1.lower().split())
    words_doc2 = set(doc2.lower().split())

    # Find the intersection of words list of doc1 & doc2
    intersection = words_doc1.intersection(words_doc2)

    # Find the union of words list of doc1 & doc2
    union = words_doc1.union(words_doc2)

    # Calculate Jaccard similarity score
    # using length of intersection set divided by length of union set
    return float(len(intersection)) / len(union)



def get_cosine_similarity(resume,job_description):
    # A list of text
    text = [resume, job_description]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)


    #Print the similarity scores
    print("\nSimilarity Scores:")
    print(cosine_similarity(count_matrix))

    #get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 4) # round to two decimal
    print("Your resume matches about "+ str(matchPercentage)+ "% of the job description.")
    return matchPercentage
class skill_keyword_match:
    def __init__(self, jobs_list):
        '''
        Initialization - converts list to DataFrame
        Input: 
            jobs_list (list): a list of all jobs info
        Output: 
            None
        '''
        print("overall dict=", overall_dict)
        self.jobs_info_df = pd.DataFrame(jobs_list)
          
    def keywords_extract(self, text): 
        '''
        Tokenize webpage text and extract keywords
        Input: 
            text (str): text to extract keywords from
        Output: 
            keywords (list): keywords extracted and filtered by pre-defined dictionary
        '''        
        # Remove non-alphabet; 3 for d3.js and + for C++
        text = re.sub("[^a-zA-Z+3]"," ", text) 
        text = text.lower().split()
        stops = set(stopwords.words("english")) #filter out stop words in english language
        text = [w for w in text if not w in stops]
        text = list(set(text))
        # We only care keywords from the pre-defined skill dictionary
        keywords = [str(word) for word in text if word in overall_dict]
        return keywords
 
    def keywords_count(self, keywords, counter): 
        '''
        Count frequency of keywords
        Input: 
            keywords (list): list of keywords
            counter (Counter)
        Output: 
            keyword_count (DataFrame index:keyword value:count)
        '''           
        keyword_count = pd.DataFrame(columns = ['Freq'])
        for each_word in keywords: 
            keyword_count.loc[each_word] = {'Freq':counter[each_word]}
        return keyword_count
    
    def exploratory_data_analysis(self):
        '''
        Exploratory data analysis
        Input: 
            None
        Output: 
            None
        '''         
        # Create a counter of keywords
        doc_freq = Counter() 
        f = [doc_freq.update(item) for item in self.jobs_info_df['keywords']]
        
        # Let's look up our pre-defined skillset vocabulary in Counter
        overall_skills_df = self.keywords_count(overall_skills_dict, doc_freq)
        # Calculate percentage of required skills in all jobs
        overall_skills_df['Freq_perc'] = (overall_skills_df['Freq'])*100/self.jobs_info_df.shape[0]
        overall_skills_df = overall_skills_df.sort_values(by='Freq_perc', ascending=False)  
        # Make bar plot 
        plt.figure(figsize=(14,8))
        overall_skills_df.iloc[0:30, overall_skills_df.columns.get_loc('Freq_perc')].plot.bar()
        plt.title('Percentage of Required Data Skills in Data Scientist Job Posts')
        plt.ylabel('Percentage Required in Jobs (%)')
        plt.xticks(rotation=30)
        plt.show()
        print(overall_skills_df.iloc[0:30, overall_skills_df.columns.get_loc('Freq_perc')])
        
        # Plot word cloud
        all_keywords_str = self.jobs_info_df['keywords'].apply(' '.join).str.cat(sep=' ')        
        # lower max_font_size, change the maximum number of word and lighten the background:
        wordcloud = WordCloud(background_color="white").generate(all_keywords_str)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()
         
        # Let's look up education requirements
        education_df = self.keywords_count(education, doc_freq)
        # Merge undergrad with bachelor
        education_df.loc['bachelor','Freq'] = education_df.loc['bachelor','Freq'] + education_df.loc['undergraduate','Freq'] 
        education_df.drop(labels='undergraduate', axis=0, inplace=True)
        # Calculate percentage of required skills in all jobs
        education_df['Freq_perc'] = (education_df['Freq'])*100/self.jobs_info_df.shape[0] 
        education_df = education_df.sort_values(by='Freq_perc', ascending=False)  
        # Make bar plot 
        plt.figure(figsize=(14,8))
        education_df['Freq_perc'].plot.bar()
        plt.title('Percentage of Required Education in Data Scientist Job Posts')
        plt.ylabel('Percentage Required in Jobs (%)')
        plt.xticks(rotation=0)
        plt.show()
        print(education_df)
        
        # Plot distributions of jobs posted in major cities
        #colors = ['#ACA7A8','#DE3163','#8A0886']
        plt.figure(figsize=(8,8))
        self.jobs_info_df['location'].value_counts().plot.pie(autopct='%1.1f%%', textprops={'fontsize': 10},labeldistance=1.15, wedgeprops = { 'linewidth' : 1, 'edgecolor' : 'white' })
        plt.title('Data Scientist Jobs in Major Saudi Cities \n\n Total {} posted jobs in last {} days'.format(self.jobs_info_df.shape[0],config.DAY_RANGE))
        plt.ylabel('')
        plt.show()
    
    def get_jaccard_sim(self, x_set, y_set): 
        '''
        Jaccard similarity or intersection over union measures similarity 
        between finite sample sets,  and is defined as size of intersection 
        divided by size of union of two sets. 
        Jaccard calculation is modified from 
        https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
        Input: 
            x_set (set)
            y_set (set)
        Output: 
            Jaccard similarity score
        '''         
        intersection = x_set.intersection(y_set)
        if len(x_set) + len(y_set) - len(intersection)!=0:
            j=float(len(intersection)) / (len(x_set) + len(y_set) - len(intersection))
        else:j=0
        return j
    
    def cal_similarity(self, resume_keywords, location=None):
        '''
        Calculate similarity between keywords from resume and job posts
        Input: 
            resume_keywords (list): resume keywords
            location (str): city to search jobs
        Output: 
            top_match (DataFrame): top job matches
        '''         
        num_jobs_return = 5
        similarity = []
        j_info = self.jobs_info_df.loc[self.jobs_info_df['location']==location].copy() if len(location)>0 else self.jobs_info_df.copy()
        if j_info.shape[0] < num_jobs_return:        
            num_jobs_return = j_info.shape[0]  
        for job_skills in j_info['keywords']:
            similarity.append(self.get_jaccard_sim(set(resume_keywords), set(job_skills)))
        j_info['similarity'] = similarity
        top_match = j_info.sort_values(by='similarity', ascending=False).head(num_jobs_return)        
        # Return top matched jobs
        return top_match
      
    def extract_jobs_keywords(self):
        '''
        Extract skill keywords from job descriptions and add a new column 
        Input: 
            None
        Output: 
            None
        ''' 
        self.jobs_info_df['keywords'] = [self.keywords_extract(job_desc) for job_desc in self.jobs_info_df['desc']]
        print("job keywords",self.jobs_info_df['keywords'])
        
    def extract_resume_keywords(self, resume_pdf): 
        '''
        Extract key skills from a resume 
        Input: 
            resume_pdf (str): path to resume PDF file
        Output: 
            resume_skills (DataFrame index:keyword value:count): keywords counts
        ''' 
        # Open resume PDF
        resume_file = open(resume_pdf, 'rb')
        # creating a pdf reader object
        resume_reader = PyPDF2.PdfFileReader(resume_file)
        # Read in each page in PDF
        resume_content = [resume_reader.getPage(x).extractText() for x in range(resume_reader.numPages)]
        #resume_content=resume_file.read()
        # Extract key skills from each page
        resume_keywords = [self.keywords_extract(page) for page in resume_content]
        # Count keywords
        resume_freq = Counter() 
        f = [resume_freq.update(item) for item in resume_keywords] 
        # Get resume skill keywords counts
        resume_skills = self.keywords_count(overall_skills_dict, resume_freq)
        print("resume skills",resume_skills)
        
        return(resume_skills[resume_skills['Freq']>0])
