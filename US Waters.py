from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import requests
import re

def wdj():
    url = 'https://www.waterdistrictjobs.com/search_jobs_all.cfm'
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    print('Running Water District Jobs')
    driver = webdriver.Chrome()
    driver.get(url)
    count = len(df)
    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "search-results")))
        page_content = BeautifulSoup(driver.page_source, 'html.parser')
        select_element = page_content.find('select', {'id': 'fPositionID'})
        selected_option = select_element.find('option', {'selected': True})
        job_category = selected_option.text.strip() if selected_option else ''
        holder = 'start'
        if job_category != holder and job_category:
            print(f'Starting Cycle {job_category}')
            holder = job_category
            working_content = page_content.find('ul', class_="search-results")
            for items in working_content.find_all('a'):
                start_time1 = time.time()
                url = items['href']
                title_element = items.find('span', class_="job-title")
                title = title_element.text.strip() if title_element else ''
                company_element = items.find('span', class_="job-company")
                company = company_element.text.strip() if company_element else ''
                location_element = items.find('span', class_="job-location")
                location = location_element.text.strip() if location_element else ''
                job_type_element = items.find('span', class_="job-status")
                job_type = job_type_element.text.strip() if job_type_element else ''
                posted_element = items.find('span', class_="job-posted-date")
                posted = posted_element.text.replace('Posted:','').strip() if posted_element else ''
                job_data = []
                job_data.append({
                    'Job Board': 'Water District Jobs',
                    'Job Title': title,
                    'Company': company,
                    'URL': url,
                    'Job Category': job_category,
                    'Job Type': job_type,
                    'Posted' : posted,
                    'Location' : location,
                })
                df.loc[count] = job_data[-1]
                count += 1
                df.to_excel(excel_filename, index=False)
                end_time1 = time.time()
                elapsed_time1 = end_time1 - start_time1
                print(f'{title} saved to {excel_filename}, runtime: {elapsed_time1:.2f} seconds')
        print('Cycle Complated')
        time.sleep(2)
        print('restarting')
        if holder == "Water Resources":
            print('TASK COMPLETED')
            break
    return 0

def wdj2():
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    full = len(df)
    count = 0
    while count != full:
        if df.at[count, 'Job Board'] == 'Water District Jobs' and pd.isnull(df.at[count, 'Job Description Text']):
            url = df.at[count, 'URL']
            response = requests.get(url)
            if response.status_code == 200:
                driver1 = response.content
                time.sleep(1.5)
                working_content1 = BeautifulSoup(driver1, 'html.parser')
                listing_info = working_content1.find('ul', class_="listing-info")
                if listing_info:
                    item_list = []
                    for item in listing_info.find_all('li'):
                        item_list.append(item)
                    org_type_element = item_list[0].find('span', class_="listing-detail")
                    org_type = org_type_element.text.strip() if org_type_element else ''
                    job_id_element = item_list[3].find('span', class_="listing-detail")
                    job_id = job_id_element.text.strip() if job_id_element else ''
                description_element = working_content1.find('div', class_="listing-desc")
                job_description_raw = description_element if description_element else ''
                job_description = description_element.text.strip() if description_element else ''
                df.at[count, 'Job ID'] = job_id
                df.at[count, 'Job Description Raw'] = job_description_raw
                df.at[count, "Job Description Text"] = job_description
                df.at[count, 'Organisation Type'] = org_type
                df.to_excel(excel_filename, index=False)
                print(f'{job_id} saved to {excel_filename}')
        count += 1
                
def wwj():
    url = 'https://www.waterandwastewaterjobs.com/search'
    driver = webdriver.Chrome()
    driver.get(url)
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    print('standby select 100 per page')
    time.sleep(5)
    count = len(df)
    user = 0
    print('Running Water and Wastewater jobs')
    while user != 1:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'scroller')))
        page_content = BeautifulSoup(driver.page_source, 'html.parser')
        working_content = page_content.find('div', class_='scroller')
        for items in working_content.find_all('div', class_='listRow'):
            start_time1 = time.time()
            title_element = items.find('div', class_='title')
            title = title_element.text.strip() if title_element else ''
            url = "https://www.waterandwastewaterjobs.com" + title_element.a['href'] if title_element else ''
            item_list = []
            details1 = items.find('div', class_='listColumn company')
            if details1:
                for item in details1.find_all('span'):
                    item_list.append(item.text.strip())
                company = item_list[0] if details1 else ''
                location = item_list[2] if details1 else ''
                posted = item_list[4] if details1 and len(item_list) > 4 else ''

            job_data = []
            job_data.append({
                'Job Board': 'Water and Wastewater jobs',
                'Job Title': title,
                'Company': company,
                'URL': url,
                'Location' : location,
                'Posted' : posted,
            })
            df.loc[count] = job_data[-1]
            count += 1
            
            end_time1 = time.time()
            elapsed_time1 = end_time1 - start_time1
            print(f'{count} {title} saved to {excel_filename}, runtime: {elapsed_time1:.2f} seconds')
        df.to_excel(excel_filename, index=False)
        user = int(input('enter 1 to end task '))
    return 0
    
def wwj2():
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    full = len(df)
    driver = webdriver.Chrome()
    count = 0
    while count != full:
        if df.at[count, 'Job Board'] == 'Water and Wastewater jobs' and pd.isnull(df.at[count, 'Job Description Text']):
            url = df.at[count, 'URL']
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "formItemContainer.widthFull.clearLeft")))
            desc_content = BeautifulSoup(driver.page_source, 'html.parser')
            description_element = desc_content.find('div', {'id':"description", 'class':"formItemContainer widthFull clearLeft"})
            job_description_raw = description_element if description_element else ''
            job_description = description_element.text.strip() if description_element else ''
            other_details = desc_content.find('div', class_='customFields')
            item_list = []
            for item in other_details.find_all('div', class_="formItemContainer"):
                item_list.append(item.text)
            for item in item_list:
                if item:
                    if 'Job Category' in item:
                        job_category = item.replace('Job Category','').strip()
                    if 'Job category' in item:
                        job_category = item.replace('Job category','').strip()
                    if 'Career Level' in item:
                        career_level = item.replace('Career Level','').strip()
                    if 'Career level' in item:
                        career_level = item.replace('Career level','').strip()
            desc_element1 = description_element.find('span', {'id':"lblOutDescription"})
            item_list = []
            for item in desc_element1.children:
                item.text.strip()
                if item:
                    item_list.append(item)
            skills_section, desc_section = '',''
            try:
                for i in range(0, len(item_list)):
                    if 'Minimum Qualifications' in item_list[i]:
                        skills_section = item_list[i+1].text.strip()
                        break
                for i in range(0, len(item_list)):
                    if "Duties and Responsibilities" or 'Essential Functions' in item_list[i]:
                        desc_section = item_list[i+1].text.strip()
                        break
            except:
                print('error with sections')
            df.at[count, 'Organisation Type'] = job_category
            df.at[count, 'Career Level']= career_level
            df.at[count, 'Job Description Raw'] = job_description_raw
            df.at[count, "Job Description Text"] = job_description
            df.at[count, 'Skill Section'] = skills_section
            df.at[count, 'Desc Section'] = desc_section
            df.to_excel(excel_filename, index=False)
            print(f'saved to {excel_filename}')
            time.sleep(1.4)
        count += 1
        
def california_department_water_resource():
    url = 'https://www.jobs.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#depid=152'
    driver = webdriver.Chrome()
    driver.get(url)
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    count = len(df)
    user = 0
    print('Running California Department of Water Resource')
    while user != 1:
        aa = int(input('enter any to start: '))
        page_content = BeautifulSoup(driver.page_source, 'html.parser')
        working_content = page_content.find('div', {'id':"cphMainContent_pnlResults", 'class':"section section-default section-search-results"})
        for job_cards in working_content.find_all('div', class_="card card-default"):
            title_element = job_cards.a
            title1 = title_element.text.strip() if title_element else ''
            url = title_element['href'] if title_element else ''
            title_element1 = job_cards.find('div', class_="working-title details row")
            title2 = title_element1.text.replace('Working Title:', '').strip() if title_element1 else ''
            if title1.lower() == title2.lower():
                title = title1
            else: title = title2 + " - " + title1
            id_element = job_cards.find('div', class_="position-number details row")
            id = id_element.text.replace('Job Control:','').strip() if id_element else ''
            salary_element = job_cards.find('div', class_='salary-range details row')
            salary = salary_element.text.replace('Salary Range:','').strip() if salary_element else ''
            work_type_element = job_cards.find('div', class_='schedule details row')
            work_type = work_type_element.text.replace('Work Type/Schedule:','').strip() if work_type_element else ''
            company_element = job_cards.find('div', class_='department details row')
            company = company_element.text.replace('Department:','').strip() if company_element else ''
            location_element = job_cards.find('div', class_="location details row")
            location = location_element.text.replace('Location:','').strip() if location_element else ''
            posted_element = job_cards.find('div', class_="filing-date details row")
            posted = posted_element.text.replace('Publish Date:','').strip() if posted_element else ''
            job_data = []
            job_data.append({
                'Job Board': 'California Department of Water Resource',
                'Job Title': title,
                'Company': company,
                'URL': url,
                'Location' : location,
                'Posted' : posted,
                'Salary' : salary,
                'Job ID' : id,
                'Job Type' : work_type
            })
            df.loc[count] = job_data[-1]
            count += 1
            print(f'{count} {title} saved to {excel_filename}')
        df.to_excel(excel_filename, index=False)
        end_time1 = time.time()
        user = int(input('enter 1 to end task: '))
    return 0

def california_department_water_resource2():
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    full = len(df)
    driver = webdriver.Chrome()
    count = 0
    while count != full:
        if df.at[count, 'Job Board'] == 'California Department of Water Resource' and pd.isnull(df.at[count, 'Job Description Text']):
            url = df.at[count, 'URL']
            id1 = df.at[count, 'Job ID']
            title = df.at[count, 'Job Title']
            id = str(int(id1)) + ' - (' + title + ")"
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h3[contains(text(), 'Job Description and Duties')]")))
            working_content = BeautifulSoup(driver.page_source, 'html.parser')
            desc_element = working_content.find('div', {'id':"pnlJobDescription"})
            job_description_raw = desc_element.span if desc_element else ''
            job_description = desc_element.span.text.strip() if desc_element else ''
            job_category_element = working_content.find('div', {'id':"pnlDepartmentInfo"})
            job_category = job_category_element.span.text.strip() if job_category_element else ''
            if desc_element.a:
                pdf_link = desc_element.a['href']
                response = requests.get(pdf_link)
                with open(fr'C:\Users\User\Desktop\hold\cali department of water pdf\{id}.pdf', 'wb') as file:
                    file.write(response.content)
            df.at[count, 'Organisation Type'] = job_category
            df.at[count, 'Job Description Raw'] = job_description_raw
            df.at[count, "Job Description Text"] = job_description
            df.to_excel(excel_filename, index=False)

            print(f'saved to {excel_filename}')
        count += 1

def laww():
    url = 'https://www.ladwp.com/who-we-are/careers'
    driver = webdriver.Chrome()
    driver.get(url)
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    count = len(df)
    user = 0
    print('Running LA water')    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for job_cards in page_content.find_all("article"):
        if job_cards.find('div', class_="coh-container card-content"):
            title_element = job_cards.h3
            job_title = title_element.text.strip() if title_element else ''
            date_element = job_cards.p
            job_date = date_element.text.strip() if date_element else ''
            link_element = job_cards.a
            job_url = link_element['href'] if link_element else ''
            job_data = []
            job_data.append({
                'Job Board': 'LA Department of Water and Power',
                'Job Title': job_title,
                'Company': 'LA Department of Water and Power',
                'URL': job_url,
                'Posted' : job_date,
                'Location' : 'Los Angeles'
            })
            df.loc[count] = job_data[-1]
            count += 1
            df.to_excel(excel_filename, index=False)
    df.to_excel(excel_filename, index=False)

def laww2():
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    full = len(df)
    driver = webdriver.Chrome()
    count = 0
    while count != full:
        if df.at[count, 'Job Board'] == 'LA Department of Water and Power' and pd.isnull(df.at[count, 'Job Description Text']):
            url = df.at[count, 'URL']
            title = df.at[count, 'Job Title']
            driver.get(url)
            page_content = BeautifulSoup(driver.page_source, 'html.parser')
            title_element = page_content.find('h1', class_="entity-title")

            summary_element = page_content.find('div', class_="summary container")
            summary_el = {}
            if summary_element:
                for lines in summary_element.find_all('dl', class_="summary-section"):
                    summary_el[lines.dt.text.strip()] = lines.dd.text.strip()
            summary_element2 = page_content.find('div', class_="row-fluid summary-section")
            if summary_element2:
                for lines in summary_element2.find_all('div', class_="row-fluid"):
                    for line in lines.findChildren():
                        item1 = line.find('div', class_='span4')
                        item2 = line.find('div', class_='span8')
                        if item1 and item2:
                            summary_el[item1.text.strip()] = item2.text.strip()
            print(summary_el)
            desc_raw = page_content.find('div', class_="container entity-details-content tab-content")
            desc_text = desc_raw.text.strip() if desc_raw else ''
            if title_element.text.strip().lower() in title.lower(): 
                job_title = title_element.text.strip()
                df.at[count, 'Job Title'] = job_title
            #df.at[count, 'Desc Section'] = summary_el
            df.at[count, 'Job Description Raw'] = desc_raw
            df.at[count, "Job Description Text"] = desc_text
            try:
                job_cat = summary_el['Department']
                df.at[count, 'Job Category'] = job_cat
            except:
                print('no job cat')
            if 'classspecs' in url:
                job_id = url[-6:]
                df.at[count, 'Job ID'] = job_id
            df.to_excel(excel_filename, index=False)
        count += 1

def mdsca(text):
    url = 'https://careers-mwdh2o.icims.com/jobs/search?hashed=-435625158'


    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    count = len(df)
    user = 0
    print('Running The Metropolitan Water District of Southern California')    
    page_content = BeautifulSoup(text, 'html.parser')
    for job_card in page_content.find_all('div', class_='row'):
        job_card_list = []
        job_location, job_id, job_title = '','',''
        for div in job_card.find_all('div'):
            job_card_list.append(div.text.strip())
        for item in job_card_list:
            if 'Job Location' in item:
                job_location = item.replace('Job Locations','').replace('\n','')
            elif 'Job ID' in item:
                job_id = item.replace('Job ID','').replace('\n','')
            elif 'Job Title' in item:
                job_title = item.replace('Job Title','').replace('\n','')
            else:
                job_summary = item
        if job_card.a: 
            job_url = job_card.a['href']
        else : job_url = ''
        job_data = []
        job_data.append({
            'Job Board': 'The Metropolitan Water District of Southern California',
            'Job Title': job_title,
            'Company': 'The Metropolitan Water District of Southern California',
            'URL': job_url,
            'Job ID' : job_id,
            'Location' : job_location
        })
        df.loc[count] = job_data[-1]
        count += 1

    df.to_excel(excel_filename, index=False)
    
def mdsca2():
    excel_filename = r'C:\Users\User\Desktop\hold\uswater.xlsx'
    df = pd.read_excel(excel_filename)
    full = len(df)
    driver = webdriver.Chrome()
    count = 0
    while count != full:
        if df.at[count, 'Job Board'] == 'The Metropolitan Water District of Southern California' and pd.isnull(df.at[count, 'Job Description Text']):
            url = df.at[count, 'URL']
            print(url)
            driver.get(url)
            time.sleep(6)
            page_content = BeautifulSoup(driver.page_source, 'html.parser')
            print(driver.page_source)
            summary_element = page_content.find('div', class_="col-xs-12 additionalFields")
            sum_el = {}
            for item in summary_element.find_all('div', class_="iCIMS_JobHeaderTag"):
                item1 = item.dt
                item2 = item.dd
                if item1 and item2:
                    sum_el[item1.text.strip()] = item2.text.strip()
            desc_raw = page_content.find('div', class_="iCIMS_InfoMsg iCIMS_InfoMsg_Job")
            job_cat_element = sum_el['Group'] + '-' + sum_el['Section']
            job_cat = job_cat_element if job_cat_element else ''
            desc_text = desc_raw.text.strip() if desc_raw else ''
            df.at[count, 'Job Category'] = job_cat
            df.at[count, 'Desc Section'] = sum_el
            df.at[count, 'Job Description Raw'] = desc_raw
            df.at[count, "Job Description Text"] = desc_text
            df.to_excel(excel_filename, index=False)
        count += 1
        
def main():
    #wdj()
    #wdj2()
    #wwj()
    #wwj2()
    #california_department_water_resource()
    #california_department_water_resource2()   
    #laww()
    laww2()
    text = """"""
    #mdsca(text)
    #mdsca2()
    
main()