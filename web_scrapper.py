# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 12:29:09 2018

@author: Peng Wang

Scrape jobs from indeed.ca
"""
import math
import random, json
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time, os
import config

# We only collect max 500 jobs from each city
max_results_per_city = 500
# Number of jobs show on each result page
page_record_limit = 50
num_pages = int(max_results_per_city/page_record_limit)

def get_jobs_info(h):
    '''
    Scrape from web or read from saved file
    Input: 
        search_location - search job in a certain city. Input from commond line.
    Output: 
        jobs_info - a list that has info of each job i.e. link, location, title, company, salary, desc
    '''
    print(config.JOBS_INFO_JSON_FILE+h+'.json')
    exists = os.path.isfile(config.JOBS_INFO_JSON_FILE+'Data Science'+'.json')

    if exists:
        print("OKKKKK",config.JOBS_INFO_JSON_FILE+'Data Science'+'.json')
        
        with open(config.JOBS_INFO_JSON_FILE+'Data Science'+'.json', 'r') as fp:
            jobs_info = json.load(fp)            
    else:
        jobs_info = web_scrape(search_location)
    return jobs_info
        
def web_scrape(search_location):
    '''
    Scrape jobs from indeed.ca
    When scraping web, be kind and patient
    Web scraping 101: http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/
    Input: 
        search_location - search job in a certain city. Input from commond line.
    Output: 
        jobs_info - a list that has info of each job i.e. link, location, title, company, salary, desc
    '''
    # urls of all jobs
    job_links = []
    # Record time for web scraping
    start = time.time() # start time
    # Launch webdriver
    driver = webdriver.Chrome(config.WEBDRIVER_PATH)
    job_locations = config.JOB_LOCATIONS
    # If search location is defined, only search that location
    if (len(search_location) > 0):
        job_locations = [search_location]
        
    # *** Extract all job urls ***
    for location in job_locations:
        url = 'https://sa.indeed.com/jobs?q='+ config.JOB_SEARCH_WORDS + '&l=' \
        + location + '&limit=' + str(page_record_limit) + '&fromage='+ str(config.DAY_RANGE)
        # Set timeout
        driver.set_page_load_timeout(15)
        webdriver.DesiredCapabilities.CHROME["unexpectedAlertBehaviour"] = "accept"
        driver.get(url)
        # Be kind and don't hit indeed server so hard
        time.sleep(3)
        #result_text=driver.find_element(By.ID, 'searchCount').text
        #list_numbers=[int(s) for s in result_text.split() if s.isdigit()]
        #num_pages = math.ceil((list_numbers[-1])/22)
        #print("number of results pages = ",num_pages)
        for i in range(num_pages):
            try:
                # For each job on the page find its url
                list_jobs=driver.find_elements(By.CLASS_NAME,'jcs-JobTitle')
                print("number of jobs = ",len(list_jobs))
                for job_each in list_jobs:
                    print("OK1")
                    job_link = job_each.get_attribute('href')
                    print("job link = ",job_link)
                    job_links.append({'location':location, 'job_link':job_link})                
                print ('scraping {} page {} success'.format(location, i+1))
                # Go next page
                driver.find_element(By.LINK_TEXT,'Next').click()
                #driver.find_element(By.CLASS_NAME,'np').click()
            except NoSuchElementException:
                # If nothing find, we are at the end of all returned results
                print("{} finished with NoSuchElementException".format(location))
                break        
            # Be kind and don't hit indeed server so hard
            time.sleep(3)
    # Write all jobs links to a json file so it can be reused later
    with open(config.JOBS_LINKS_JSON_FILE, 'w') as fp:
        json.dump(job_links, fp)
        
    # ***Go through each job url and gather detailed job info ***
    # Info of all jobs
    jobs_info = []
    # Opening JSON links file
    exists = os.path.isfile(config.JOBS_LINKS_JSON_FILE)
    if exists:
        with open(config.JOBS_LINKS_JSON_FILE, 'r') as fp:
            job_links = json.load(fp)


    for job_lk in job_links:
        # Make some random wait time between each page so we don't get banned 
        m = random.randint(1,5)
        time.sleep(m) 
        # Retrieve single job url
        link = job_lk['job_link'] 
        driver.get(link)
        time.sleep(3)
        # Job city and province
        location = job_lk['location']
        # Job title
        title = driver.find_element(By.XPATH,'//*[@id="viewJobSSRRoot"]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[1]').text
        # Company posted the job
        company = driver.find_element(By.XPATH,'//*[@id="viewJobSSRRoot"]/div[2]/div/div[3]/div/div/div[1]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[1]/div[2]/div').text
        # Salary: if no such info, assign NaN
        if (len(driver.find_elements(By.XPATH,'//*[@id="jobDetailsSection"]/div[2]/span'))==0):
            salary = np.nan 
        else:
            salary = driver.find_element(By.XPATH,'//*[@id="jobDetailsSection"]/div[2]/span').text
        # Job description
        desc = driver.find_element(By.XPATH,'//*[@id="jobDescriptionText"]').text
        jobs_info.append({'link':link, 'location':location, 'title':title, 'company':company, 'salary':salary, 'desc':desc})
    # Write all jobs info to a json file so it can be re-used later
    with open(config.JOBS_INFO_JSON_FILE+'.json', 'w') as fp:
        json.dump(jobs_info, fp)
    # Close and quit webdriver
    driver.quit()    
    end = time.time() # end time
    # Calculate web scaping time
    scaping_time = (end-start)/60.
    print('Took {0:.2f} minutes scraping {1:d} data scientist/engineer/analyst jobs'.format(scaping_time, len(jobs_info)))
    return jobs_info