# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:35:00 2018

@author: Peng Wang

Build a simple data-science-skill-keyword-based job recommendation engine, 
which match keywords from resume to data science jobs in major Canadian cities.
Step 1: Scrape "data scientist/engineer/analyst" jobs from indeed.ca
Step 2: Tokenize and extract skill keywords from job descriptions
Step 3: Tokenize and extract skill keywords from resume
Step 4: Calculate Jaccard similarity of keywords from posted jobs and resume, 
        and recommend top 5 matches 
"""
import sys

#from IPython.display import display

import config, web_scrapper,utils
from skill_keyword_match import skill_keyword_match,get_cosine_similarity
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import os

def main():
    # If city included, only search and recommend jobs in the city
    location = ''
    if (len(sys.argv) > 1):
        # Check if input city name matches our pre-defined list
        if (sys.argv[1] in config.JOB_LOCATIONS):
            location = sys.argv[1]
        else:
            sys.exit('*** Please try again. *** \nEither leave it blank or input a city from this list:\n{}'.format('\n'.join(config.JOB_LOCATIONS)))
    # ---------------------------------------------------
    # ---- Scrape from web or read from local saved -----
    # ---------------------------------------------------
    #read dataset of resumes
    df = pd.read_csv(r'./data/UpdatedResumeDataSet.csv')
    df=df.loc[df['Category'].isin(['Data Science','Civil Engineer','Electrical Engineering','Network Security Engineer','Sales'])]
    #print(df)
    Y_true=[]
    Y_pred=[]
    for ind in df.index:
        resume_text=df['Resume'][ind]
        Y_true.append(config.IT_JOBS.index(df['Category'][ind]))
        list_sim = []
        #print(Y_true,resume_text)
    #print(Y_true)
        result = pd.DataFrame()
        for f in config.IT_JOBS:
            # print(f)
            jobs_info = web_scrapper.get_jobs_info(f)
            #print("OK", f)
            #print(jobs_info)

            for i in jobs_info:
                list_sim.append({'job':f,"similarity":get_cosine_similarity(resume_text, i['desc'])})
        print(list_sim)
        result_=pd.DataFrame(list_sim)
        result_ = result_.sort_values(by='similarity', ascending=False)
        result_ = result_.iloc[0:5]
        #result__ = result_['job'].mode()  # to extract the frequent job class
        selected_job = result_['job'].values[0]
        print(result_)
        Y_pred.append(config.IT_JOBS.index(selected_job))
    print("Y_true= ",Y_true)
    print('Y_pred= ', Y_pred)
    data3 = {'Actual_job': Y_true, 'Predicted_job': Y_pred}
    df3 = pd.DataFrame(data3, columns=['Actual_job', 'Predicted_job'])
    confusion_matrix = pd.crosstab(df3['Actual_job'], df3['Predicted_job'], rownames=['Actual'], colnames=['Predicted'])
    print(classification_report(Y_true,Y_pred))
    '''print('Precision: %.3f' % precision_score(Y_true, Y_pred))
    print('Recall: %.3f' % recall_score(Y_true, Y_pred))
    print('Accuracy: %.3f' % accuracy_score(Y_true, Y_pred))
    print('F1 Score: %.3f' % f1_score(Y_true, Y_pred))'''

    sn.heatmap(confusion_matrix, annot=True)
    plt.show()

if __name__ == "__main__": 
    main()
    
    