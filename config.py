# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:26:22 2018

@author: Peng Wang
"""
# Saved file for each job url
JOBS_LINKS_JSON_FILE = r'./data/indeed_jobs_links.json'
# Saved file for each job info
JOBS_INFO_JSON_FILE = r'./data/indeed_jobs_info '
# Saved file for recommended jobs
RECOMMENDED_JOBS_FILE = r'./data/recommended_jobs'
# Path to webdriver exe
WEBDRIVER_PATH = r'C:/Users/fer_i/Downloads/chromedriver_win32/chromedriver.exe'
# Cities to search: 6 largest Canadian cities

JOB_LOCATIONS = ['Dammam', 'Jeddah', 'Riyadh']
# Seach "data scientist" OR "data+engineer" OR "data+analyst" with quotation marks
#JOB_SEARCH_WORDS = '"data scientist"+OR+"data engineer"+OR+"data analyst"'
#JOB_SEARCH_WORDS = ''"rehabilitation"+' OR '+"nurse"+' OR '+"health"''
JOB_SEARCH_WORDS = "Data Science"
#'data analyst'
#'Database Administrator'
#'IT Consultant'
#'Full Stack Developer'
#'Network Architect'
# To avoid same job posted multiple times, we only look back for 30 days
DAY_RANGE = 30
# Path to sample resume
#SAMPLE_RESUME_PDF = # Path to sample resume
SAMPLE_RESUME_PDF = r'./data/PWang_resume.pdf'
#JOBS_INFO_FILES=['Data_Analyst.json','Database_Administrator.json','Full_Stack_Developer.json','IT_Consultant.json','Network_Architect.json']
DATASET_DIR= r'./data/CV_dataset3'
IT_JOBS=['Network Security Engineer']
#,'Civil Engineer','Network Security Engineer','Sales','Electrical Engineering']
#'Health and fitness',
#'Web Designing'
#['Banking','IT']
#IT_JOBS=['Full_Stack_Developer','IT_Consultant','Network_Architect','Database_Administrator','Design_Engineer']
#'Data_Analyst'
#Full_Stack_Developer
#'Civil Engineer','network security engineer','web designer','sales engineer','healthcare'