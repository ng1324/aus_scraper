from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import requests
import re

def iconwater(url, count):
    print('Running iconwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)

    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="table-responsive")
    job_container = job_container.find('tbody')
    job_data = []
    
    for job_post in job_container.find_all('tr'):
        job_id = job_post.get('id')
        job_url = "https://recruitment.iconwater.com.au/ProductionWC/jobs1/vacancies/" + job_id + "/edit"
        job_title_element = job_post.find('td', {'class': 'text', 'data-th': 'Position'})
        job_title = job_title_element.text.strip() if job_title_element else ''
        job_location_element = job_post.find('td', {'class': "text", 'data-th': "Location"})
        job_location = job_location_element.text.strip() if job_location_element else ''
        job_type_element = job_post.find('td', {'class':"text", 'data-th': "Tenure"})
        job_type = job_type_element.text.strip() if job_type_element else ''
        job_post_element = job_post.find('td', class_="date")
        posted = job_post_element.text.strip() if job_post_element else ''
        if job_url:
            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            page_content1 = BeautifulSoup(driver1, 'html.parser')
            job_cat_element = page_content1.find('div', {'class':"form-group row", 'id':"T303F020_ORGANISATION_UNIT-ct"})
            job_categories = job_cat_element.find('input').get('value')
            job_description_element = page_content1.find('div',{'class':"form-group row", 'id':"T303F270_VACANCY_SYNOPSIS-ct"})
            job_description = job_description_element.text.strip()
            job_data.append({
                'Company' : "Icon Water",
                'Job ID' : job_id,
                'Job Title': job_title,
                'Posted date' : posted,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : job_type,
                'Job Categories' : job_categories,
                'Job Summary' : '',
                'Job Description Raw' : job_description_element,
                'Job Description Text' : job_description
            })
                 
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = 'iconwater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"icon water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def hunterwater(url, count):
    print('Running hunterwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="p-gridcol col-12-device-none col-9-device-sm")
    job_data = []

    for job_post in job_container.find_all('div', class_="p-panel p-p-b-md"):
        job_title_element = job_post.a
        if job_title_element:
            job_title = job_title_element.text
            job_url = "https://hunterwater.csod.com" + job_post.a['href'] 
            posted = job_post.find('p', {'data-tag':"displayJobPostingDate"}).text
            job_location = job_post.find('p', {'data-tag':"displayJobLocation"}).text
            if job_url:
                driver1.get(job_url)
                element = WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "p-view-jobdetailsad")))
                time.sleep(1)
                page_content1 = BeautifulSoup(driver1.page_source, 'html.parser')
                title_element = page_content1.find('div', class_ = "p-panel p-p-t-sm p-p-b-md")
                job_id = title_element.find('span', {'data-tag':"ReqId"}).text
                job_description_raw = page_content1.find('div', class_="p-view-jobdetailsad")
                job_description = job_description_raw.text
            job_data.append({
                'Company' : "Hunter Water",
                'Job ID' : job_id,
                'Job Title': job_title,
                'Posted date' : posted,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : '',
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = 'hunter.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"icon water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def sunwater(url,count):
    print('Running sunwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)

    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_='container py-3 px-0')

    job_data = []

    for job_post in job_container.find_all('div', class_='col-lg-4 col-md-4 col-sm-6 py-3'):
        try:
            job_title_element = job_post.find('h5', class_="card-title").find('a', class_="job-link")
            job_title = job_title_element.text
            job_url = "https://careers.sunwater.com.au/" + job_title_element['href']
            job_location_element = job_post.find('li', class_="list-group-item border-0 py-1").find('span', class_="location")
            job_location = job_location_element.text if job_location_element else ''
            work_type_element = job_post.find('ul', class_="list-group list-group-flush border-0")
            work_type = ''
            work_type = work_type_element.find('span', class_="work-type full-time")
            if work_type: 
                work_type = work_type.text
            else: 
                work_type = work_type_element.find('span', class_="work-type casual").text
            job_summary_element = job_post.find('p', class_="card-text summary-wrap summary-wrap-2")
            job_summary = job_summary_element.text if job_summary_element else ''

            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            try: 
                page_content1 = BeautifulSoup(driver1, 'html.parser')
                title_element = page_content1.find('div', class_="col-lg-3 order-lg-2 mb-7 mb-lg-0")
                title_element = title_element.find('ul', class_='list-unstyled')
                job_location_more_element = title_element.find('span', class_="location")
                job_location_more = job_location_more_element.text if job_location_more_element else ''
                job_categories_element = title_element.find('span', class_="categories")
                job_categories = job_categories_element.text if job_categories_element else ''
                job_details_element = page_content1.find('div', class_="col-lg-9 order-lg-1")
                job_description_raw = job_details_element.find('div', id="job-details")
                if job_description_raw:
                    # Find all <p> and <li> elements within the job-details div
                    paragraphs = job_description_raw.find_all(['p', 'li'])
                    job_description = ''
                    # Extract and print the text content with formatting for pointers
                    for paragraph in paragraphs:
                        text_content = paragraph.text.strip()
                        job_description = job_description + f'\n{text_content}'
            except Exception as e:
                print(f"Error with page: {count}, {job_url}, Error {str(e)}")  
                
            job_data.append({
                'Company' : "Sun Water",
                'Job ID' : '',
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : work_type,
                'Job Categories' : job_categories,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_url}')
            count += 1
        except Exception as e:
            print(f"Error with sunwater main: {str(e)}")
        finally:
            driver.quit()

    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\sunwater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"Sunwater complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def goulburn_murray_water(url, count):
    print('Running goulburn_murray_water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', id='Articles_gmw_positions-vacant')

    job_data = []
    
    for job_post in job_container.find_all('div', class_="item article ct-web_page original-thumbs Default urlid-positions-vacant"):
        try:
            job_title_element = job_post.find('h2', class_="title")
            if job_title_element:
                job_title = job_title_element.text.strip()
                job_url = "https://www.g-mwater.com.au" + job_title_element.a['href']
            else:
                job_title = ''
                job_url = ''
            job_summary_element = job_post.find('div', class_="summary")
            job_summary = job_summary_element.text.strip() if job_summary_element else ''
            
            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            try:
                page_content1 = BeautifulSoup(driver1, 'html.parser')
                job_description_element = page_content1.find('div',id="PageBody")
                job_description_raw = job_description_element if job_description_element else ''
                job_description = job_description_element.text if job_description_element else ''
                attachment_element = page_content1.find('div', class_="attachments-container")

                        
            except Exception as e:
                print(f"Error with page: {count}, {job_url}, Error {str(e)}")
                
            job_data.append({
                'Company' : "goulburn_murray_water",
                'Job Title': job_title,
                'URL': job_url,
                'Summary': job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_url}')
            count += 1
        except Exception as e:
            print(f"Error with goulburn_murray_water main: {str(e)}")
            
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\goulburn_murray_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"goulburn_murray_water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def seq_water(url, count):
    print('Running Seqwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('tbody', id='recent-jobs-content')

    job_data = []
    
    for job_post in job_container.find_all('tr', class_="summary"):
        try:
            job_url = "https://careers.seqwater.com.au" + job_post.a['href']
            job_summary_element = job_post.find('tr', class_="summary")
            job_summary = job_summary_element.text.strip().replace('Read More >','') if job_summary_element else ''
            
            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            try:
                page_content1 = BeautifulSoup(driver1, 'html.parser')
                job_description_element = page_content1.find('div',id="job-content")
                job_title_element = job_description_element.find('h3', style = "line-height:1.2em;")
                job_title = job_title_element.text.strip() if job_title_element else ''
                job_location_element = job_description_element.find('span', class_= 'location')
                job_location = job_location_element.text.strip() if job_location_element else ''
                work_type_element = job_description_element.find('span', class_='work-type permanent')
                work_type = work_type_element.text.strip() if work_type_element else ''
                job_categories_element = job_description_element.find('span', class_='categories')
                job_categories = job_categories_element.text.strip() if job_categories_element else ''
                
                job_description_element1 = job_description_element.find('div', id='job-details')
                job_description_raw = job_description_element1 if job_description_element1 else ''
                job_description = job_description_element1.text if job_description_element1 else ''
            except Exception as e:
                print(f"Error with page: {count}, {job_url}, Error {str(e)}")

            job_data.append({
                'Company' : "SEQ Water",
                'Job ID' : '',
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : work_type,
                'Job Categories' : job_categories,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_url}')
            count += 1
        except Exception as e:
            print(f"Error with seq_water main: {str(e)}")
            
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\seqwater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"Seqwater complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def south_east_water(url, count):
    print('Running South east water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="searchResultsShell")

    job_data = []
    
    for job_post in job_container.find_all('tr', class_="data-row"):
        try:
            job_title_element = job_post.find('span', class_="jobTitle hidden-phone")
            job_title = job_title_element.text.strip() if job_title_element else ''
            job_url = "https://jobs.southeastwater.com.au/" + job_title_element.a['href']
            job_location_element = job_post.find('td', class_="colLocation hidden-phone", headers="hdrLocation")
            job_location = job_location_element.text.strip() if job_location_element else ''
            response = requests.get(job_url)

            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            try:
                page_content1 = BeautifulSoup(driver1, 'html.parser')
                job_description_element = page_content1.find('span', class_="jobdescription")
                job_description_raw = job_description_element if job_description_element else ''
                job_description = job_description_element.text if job_description_element else ''
            except Exception as e:
                print(f"Error with page: {count}, {job_url}, Error {str(e)}")

            job_data.append({
                'Company' : "South east water",
                'Job ID' : '',
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : '',
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_url}')
            count += 1
        except Exception as e:
            print(f"Error with South east water main: {str(e)}")
            
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\south_east_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"South east water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def urban_utilities(url, count):
    print('Running urban_utilities')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    data_rows = soup.find_all('tr')
    job_data = []
    for row in data_rows:
        # Extract the title and URL
        title_element = row.find('a', class_='job-link')
        if title_element:
            job_title = title_element.text.strip()
            job_url = "https://careers.pageuppeople.com" + title_element['href']  # Replace example.com with the actual base URL
            location_element = row.find('span', class_='location')
            job_location = location_element.text.strip() if location_element else ''
            summary_element = row.find_next_sibling('tr', class_='summary')
            job_summary = summary_element.td.text.strip() if summary_element else ''
        
            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {url}: {response.status_code}")
            try:
                page_content1 = BeautifulSoup(driver1, 'html.parser')
                job_description_element = page_content1.find('div', id="job-content")
                job_id_element = job_description_element.find('span', class_='job-externalJobNo')
                job_id = job_id_element.text.strip() if job_id_element else ''
                work_type_element = job_description_element.find('span', class_="work-type permanent-full-time")
                work_type_element1 = job_description_element.find('span', class_="work-type temporary-full-time")
                work_type_element2 = job_description_element.find('span', class_="work-type permanent-full-time various-opportunities")
                work_type = ''
                if work_type_element:
                    work_type = work_type_element.text.strip()
                elif work_type_element1: 
                    work_type = work_type_element1.text.strip()
                elif work_type_element2:
                    work_type = work_type_element2.text.strip()
                job_categories_element = job_description_element.find('span', class_="categories")
                job_categories = job_categories_element.text.strip() if job_categories_element else ''
                job_description_content = job_description_element.find('div', id='job-details')
                job_description_raw = job_description_content if job_description_content else ''
                job_description = job_description_content.text if job_description_content else ''
            except Exception as e:
                print(f"Error with page:  {job_url}, Error {str(e)}")
                
            print(f'Job {count} pulled for: {job_url}')
            count += 1
            job_data.append({
                'Company' : "urban utilities",
                'Job ID' : job_id,
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : work_type,
                'Job Categories' : job_categories,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })

    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\urban_utilities.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"urban_utilities complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def water_corp(url, count):
    print('Running water_corp')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="ftllist", id="requisitionListInterface.listRequisitionContainer")
    job_data = []
    job_count_element = page_content.find('div', class_="resultstitlepanel")
    job_count_element = job_count_element.find('span', id="requisitionListInterface.ID829", class_="subtitle").text
    job_count = int(re.search(r'\d+', job_count_element).group())
    print(job_count)
    wait = WebDriverWait(driver, 10)  # Adjust the timeout (10 seconds in this case)
    element = wait.until(EC.element_to_be_clickable((By.ID, "requisitionListInterface.reqTitleLinkAction.row1")))
    
    if element:
        for _ in range(job_count):
            element.click()
            wait.until(EC.presence_of_element_located((By.ID, "requisitionDescriptionInterface.reqTitleLinkAction.row1")))
            page_content = BeautifulSoup(driver.page_source, 'html.parser')
            job_title_element = page_content.find('span', {'id': 'requisitionDescriptionInterface.reqTitleLinkAction.row1'})
            job_title = job_title_element.get_text() if job_title_element else ""
            job_id_element = page_content.find('span', {'id': 'requisitionDescriptionInterface.reqContestNumberValue.row1'})
            job_id = job_id_element.get_text() if job_id_element else ""
            location_element = page_content.find('span', {'id': 'requisitionDescriptionInterface.ID1457.row1'})
            job_location = location_element.get_text() if location_element else ""
            organization_element = page_content.find('span', {'id': 'requisitionDescriptionInterface.ID1545.row1'})
            job_categories = organization_element.get_text() if organization_element else ""
            job_description_element = page_content.find('div', {'id': "requisitionDescriptionInterface.ID1578.row1"})
            job_description_raw = job_description_element if job_description_element else ""
            job_description = job_description_raw.text.strip()
            
            job_data.append({
                'Company' : "water corp",
                'Job ID': job_id,
                'Job Title': job_title,
                'Posted date': '',
                'URL': '',
                'Job Location': job_location,
                'Work Type': '',
                'Job Categories': job_categories,
                'Job Summary': '',
                'Job Description Raw': job_description_raw,
                'Job Description Text': job_description
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
            wait = WebDriverWait(driver, 10)  # Adjust the timeout (10 seconds in this case)
            element = wait.until(EC.element_to_be_clickable((By.ID, "requisitionDescriptionInterface.pagerDivID771.Next")))
            time.sleep(1.5)
            element.click()
            
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\water_corp.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"water_corp complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def melbourne_water(url, count):
    print('Running melbourne_water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    job_data = []
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="job-listing-wrapper")
    for job_cards in job_container.find_all('li', class_="jobs-item"):
        job_title_element = job_cards.find('a', class_="job-link")
        job_title = job_title_element.text.strip() if job_title_element else ''
        job_url = job_title_element['href'] if job_title_element else ''
        job_url = "https://careers.pageuppeople.com" + job_url
        work_type_element = job_cards.find('span', class_="work-type")
        work_type = work_type_element.text.strip() if work_type_element else ''
        job_location_element = job_cards.find('span', class_="location")
        job_location = job_location_element.text.strip() if job_location_element else ''
        job_summary_element = job_cards.find('p', class_="jobs-summary")
        job_summary = job_summary_element.text.strip() if job_summary_element else ''
        
        if job_url:
            try:
                response = requests.get(job_url)
                if response.status_code == 200:
                    driver1 = response.content
                    page_content1 = BeautifulSoup(driver1, 'html.parser')
                    page_content_element = page_content1.find('div', class_="region container region-content")
                    job_id_element = page_content_element.find('span', class_="job-externalJobNo")
                    job_id = job_id_element.text.strip() if job_id_element else ''
                    job_categories_element = page_content_element.find('span', class_="categories")
                    job_categories = job_categories_element.text.strip() if job_categories_element else ''
                    job_description_element = page_content_element.find('div', {'id':"job-details"})
                    job_description_raw = job_description_element
                    job_description = job_description_raw.text.strip()
                else:
                    print(f"Error getting HTML for {job_url}: {response.status_code}")
            except Exception as e:
                print(f"Error with page:  {url}, Error {str(e)}")
            job_data.append({
                'Company' : "melbourne water",
                'Job ID' : job_id,
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : work_type,
                'Job Categories' : job_categories,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
                 
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\melbourne_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"melbourne_water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def barwon_water(url, count):
    print('Running barwon_water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver.get(url)
    job_data = []
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="job-listing")
    for job_cards in job_container.find_all('div', class_="job-listing__item"):
        job_title_element = job_cards.find('h2')
        job_title = job_title_element.text.strip() if job_title_element else ''
        details_element = job_cards.find('ul').text
        statuses_index = details_element.find("Statuses:")
        if statuses_index != -1:
            job_location = details_element[:statuses_index].strip()
            work_type = details_element[statuses_index + len("Statuses:"):].strip()
        else:
            job_location = ''
            work_type = ''
        job_url_element = job_cards.a['href']
        job_url = job_url_element if job_url_element else ''
        print(job_url)
        if job_url:
            driver1 = webdriver.Chrome()
            driver1.get(job_url)
            driver_page = BeautifulSoup(driver1.page_source, 'html.parser')
            if driver_page:
                job_description_element = driver_page.find('div', class_="job-listing__description")
                while job_description_element is None:
                    time.sleep(1)
                    job_description_element = driver_page.find('div', class_="job-listing__description")
                job_description_raw = job_description_element
                job_description = job_description_raw.text.strip()
            else:
                print(f"Error getting HTML for {job_url}")

            job_data.append({
                'Company' : "barwon_water",
                'Job ID' : '',
                'Job Title': job_title,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : work_type,
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
                 
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\barwon_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"barwon_water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def greater_western_water(url, count):
    print('Running greater_western_water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    driver.get(url)
    job_data = []
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', class_="searchResultsShell")
    for job_cards in job_container.find_all('tr', class_="data-row"):
        job_title_element = job_cards.find('span', class_="jobTitle hidden-phone")
        job_title = job_title_element.text.strip() if job_title_element else ''
        job_url = job_title_element.a['href'] if job_title_element else ''
        job_url = "https://careers.gww.com.au" + job_url
        job_location_element = job_cards.find('span', class_="jobLocation visible-phone")
        job_location = job_location_element.text.strip() if job_location_element else ''
        posted_date_element = job_cards.find('span', class_="jobDate visible-phone")
        posted_date = posted_date_element.text.strip() if posted_date_element else ''
        
        if job_url:
            try:
                driver1.get(job_url)
                driver_page = BeautifulSoup(driver1.page_source, 'html.parser')
                if driver_page:
                    job_description_element = driver_page.find('span', class_="jobdescription")
                    job_description_raw = job_description_element
                    job_description = job_description_raw.text.strip()
                else:
                    print(f"Error getting HTML for {job_url}")
            except Exception as e:
                print(f"Error with page:  {job_url}, Error {str(e)}")
            job_data.append({
                'Company' : "Greater Western Water",
                'Job ID' : '',
                'Job Title': job_title,
                'Posted date' : posted_date,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : '',
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
                 
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\greater_western_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"greater_western_water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def sa_water(url, count):
    print('Running sa_water')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    driver.get(url)
    job_data = []
    print('ATTENTION! Prepare to click on show more if available waitng 15 seconds')
    time.sleep(15)
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for job_cards in page_content.find_all("div", class_="col-12 job-search-results-card-col"):
        job_title_element = job_cards.a
        job_title = job_title_element.text.strip()
        print(job_title)
        job_url = job_title_element['href']
        print(job_url)
        job_location_element = job_cards.find('div', class_="job-component-list job-component-list-location")
        job_location = job_location_element.text.strip() if job_location_element else ''
        print(job_location)
        job_category_element = job_cards.find('div', class_="job-component-list job-component-list-category")
        job_category = job_category_element.text.strip() if job_category_element else ''
        print(job_category)
        job_type_element = job_cards.find('div', class_="job-component-list job-component-list-employment_type")
        job_type = job_type_element.text.strip() if job_type_element else ''
        print(job_type)
        job_summary_element = job_cards.find('p', {'class':"card-text job-search-results-summary", 'id':"summary_1_0_0"})
        job_summary = job_summary_element.text.strip() if job_summary_element else ''
        print(job_summary)


        if job_url:
            try:
                driver1.get(job_url)

                # Wait up to 10 seconds for the specific element to be present
                WebDriverWait(driver1, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.job-component-icon-and-text.job-component-requisition-identifier'))
                )

                page_content1 = BeautifulSoup(driver1.page_source, 'html.parser')
                job_id_element = page_content1.find('li', class_="job-component-icon-and-text job-component-requisition-identifier")
                job_id = job_id_element.text.strip() if job_id_element else ''
                job_description_element = page_content1.find('div', class_="job-description")
                job_description_raw = job_description_element if job_description_element else ''
                job_description = job_description_element.text.strip() if job_description_element else ''
                print(job_id)
                print(job_description)
            except Exception as e:
                print(f"Error with page: {job_url}, Error {str(e)}")
            job_data.append({
                'Company' : "SA Water",
                'Job ID' : job_id,
                'Job Title': job_title,
                'Posted date' : '',
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : '',
                'Job Categories' : job_category,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\sa_water.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"sa_water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def taswater(url, count):
    print('Running taswater')
    start_time = time.time()

    # Initialize a WebDriver
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    driver1 = webdriver.Chrome()
    job_data = []

    # Parse the initial page
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', {'class': "p-panel p-p-v-lg"})

    for job_cards in job_container.find_all('div', class_="p-panel p-p-b-md"):
        job_url_element = job_cards.find('a', {'class': "p-link p-f-sz-d p-link-def p-t-full-hv-primary50 p-f-w-6", 'data-tag': "displayJobTitle"})
        
        if job_url_element:
            job_url = "https://taswater.csod.com" + job_url_element['href']
            job_title = job_url_element.text.strip()
            posted_data_element = job_cards.find('p', {"data-tag": "displayJobPostingDate"})
            posted_date = posted_data_element.text.strip() if posted_data_element else ''

            # Initialize a new WebDriver for the job details
            
            driver1.get(job_url)
            time.sleep(6)
            #WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'p-panel p-p-t-xs')))
            page_content1 = BeautifulSoup(driver1.page_source, 'html.parser')

            job_id = ''
            job_location = ''
            job_description = ''
            job_description_raw = ''
            
            try:
                job_description_element = page_content1.find('div', class_="p-view-pagetemplate")
                banner_element = job_description_element.find('div', class_="p-panel p-p-v-xl")
                job_id_element = banner_element.find('span', {"data-tag": "ReqId"})
                job_id = job_id_element.text.strip() if job_id_element else ''
                location_element = banner_element.find('span', {"data-tag": "displayLocationMessage"})
                if "available" in location_element.text:
                    location_element = job_description_element.find('div', class_="p-gridlayout cols-12-device-none cols-6-device-md gutter-horizontal-lg-device-none")
                    job_location = ' '.join(location.text.strip().replace("Tasmania", "") for location in location_element.find_all('div'))
                else:
                    job_location = location_element.text.strip()
                job_description_element = page_content1.find('div', class_="p-panel p-p-t-xs")
                job_description_raw = job_description_element if job_description_element else ''
                job_description = job_description_raw.text if job_description_element else ''

            except Exception as e:
                print(f"Error with page: {count}, {job_url}, Error {str(e)}")

            job_data.append({
                'Company': "taswater",
                'Job ID': job_id,
                'Job Title': job_title,
                'Posted date': posted_date,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type': '',
                'Job Categories': '',
                'Job Summary': '',
                'Job Description Raw': job_description_raw,
                'Job Description Text': job_description
            })

            print(f'Job {count} pulled for: {job_title}')
            count += 1

            # Close the second WebDriver
            driver1.quit()

    # Close the first WebDriver
    driver.quit()

    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\taswater.xlsx'
    df.to_excel(excel_filename, index=False)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f'Data saved to {excel_filename}')
    print(f"taswater complete, runtime: {elapsed_time:.2f} seconds")
    
    return count

def unitywater(url, count):
    print('Running unitywater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    driver.get(url)
    job_data = []
    time.sleep(5)
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "refari-job-item-wrapper")))
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for items in page_content.find_all('div', class_="refari-job-item-wrapper"):
        posted_element = items.find('div', class_="refari-job-item-posted-at").text.strip()
        posted = ''
        for char in posted_element:
            if char.isdigit():
                posted = posted + char
        posted = int(posted)
        job_title_element = items.find('div', class_="MuiCardHeader-root refari-job-item-title-wrap")
        job_element = []
        for sections in job_title_element.find_all('span'):
            job_element.append(sections)
        job_title = job_element[0].text.strip()
        job_url = job_element[0].a['href']
        job_category = job_element[2].text.strip()
        job_summary_element = items.find('div', class_="refari-job-item-description")
        job_summary = job_summary_element.text.strip() if job_summary_element else ''
        other_elements = items.find('div', class_="refari-job-item-subtitle-wrap")
        job_element = []
        for sections in other_elements.find_all('li'):
            job_element.append(sections.text.strip())
        job_location = job_element[0]
        job_type = job_element[1]
        if job_url:
            driver1.get(job_url)
            element = WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "refari-job-item-description")))
            page_content = BeautifulSoup(driver1.page_source, 'html.parser')
            job_description_raw = page_content.find('div', class_="refari-job-item-description")
            job_description = job_description_raw.text.strip() if job_description_raw else ''
        job_data.append({
            'Company' : "Unity Water",
            'Job ID' : '',
            'Job Title': job_title,
            'Posted date' : posted,
            'URL': job_url,
            'Job Location': job_location,
            'Work Type' : job_type,
            'Job Categories' : job_category,
            'Job Summary' : job_summary,
            'Job Description Raw' : job_description_raw,
            'Job Description Text' : job_description
        })
                
        print(f'Job {count} pulled for: {job_title}')
        count += 1
    df = pd.DataFrame(job_data)
    excel_filename = 'Unitywater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"Unity water complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def sydneywater(url, count):
    print('Running sydneywater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    job_data = []
    driver.get(url)
    while True:
        try:
            wait = WebDriverWait(driver, 10)
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "button.p-ghost-button.bright-blue")))
            button.click()
            time.sleep(4)
        except:
            break
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    job_container = page_content.find('div', {'id':"job-listings"})
    for job_cards in job_container.find_all('li'):
        header_element = job_cards.find('div', {"_ngcontent-careers-app-c12":"", "class":"content"})
        if header_element:
            job_url = 'https://talent.sydneywater.com.au' + job_cards.a['href']
            job_title = header_element.find('h3', {'_ngcontent-careers-app-c12':''}).text
            job_summary = header_element.find('p', {'_ngcontent-careers-app-c12':"", "class":"description"}).text
            other_element = job_cards.find('job-highlights')
            count_in_sydney = 1
            for items in other_element.find_all('div', {'_ngcontent-careers-app-c21':"", 'class':"highlight"}):
                items_value = items.find(class_="value")
                if count_in_sydney == 1:
                    job_location = items_value.text
                    count_in_sydney = 2
                elif count_in_sydney == 2:
                    job_type = items_value.text
            driver1.get(job_url)
            page_content1 = BeautifulSoup(driver1.page_source, 'html.parser')    
            details_element = page_content1.find('div', {'_ngcontent-careers-app-c14':"", 'id':"job-info"})
            holderlist = []
            for items in details_element.find_all('div'):
                holderlist.append(items.text.strip())
            job_id = holderlist[0].replace('Job no: ','')
            job_category = holderlist[1].replace('Category: ','')
            job_description_raw = page_content1.find('div', {'_ngcontent-careers-app-c14':"", 'class':"is-html", 'id':"job-description"})
            job_description = job_description_raw.text
            pdflink_element = page_content1.find('li', class_="attachment")
            pdf_link = pdflink_element.a['href'] if pdflink_element else ''
            try:
                response = requests.get(pdf_link)
                with open(fr'C:\Users\User\Desktop\New folder (4)\sydney water jobs\{job_id}.pdf', 'wb') as file:
                    file.write(response.content)
            except: 
                print(f'no pdf for job {job_id} {job_title}')
            job_data.append({
                'Company' : "Sydney Water",
                'Job ID' : job_id,
                'Job Title': job_title,
                'Posted date' : '',
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : '',
                'Job Categories' : job_category,
                'Job Summary' : job_summary,
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\sydneywater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"sydneywater complete, runtime: {elapsed_time1:.2f} seconds")
    return count


def waternsw(url, count, text):
    print('Running waternsw')
    start_time1 = time.time()
    #driver = webdriver.Chrome()
    job_data = []
    #driver.get(url)
    time.sleep(3)
    page_content = BeautifulSoup(text, 'html.parser')
    job_container = page_content.find('div', class_="row no-gutters")
    job_data = []
    for job_post in job_container.find_all('div', class_="col-sm-4"):
        job_title_element = job_post.find('a', class_="job_title")
        job_title = job_title_element.text.strip() if job_title_element else ''
        job_location_element = job_post.find('span', class_="location")
        job_location = job_location_element.text.replace("Location: ",'').strip() if job_location_element else ''
        job_type_element = job_post.find('span', class_="employment_status")
        job_type = job_type_element.text.replace("Job Type: ",'').strip() if job_type_element else ''
        posted_element = job_post.find('span', class_="created_at")
        posted = posted_element.text.replace("Date Posted: ",'').strip() if posted_element else ''
        job_url = job_title_element['href']
        if job_url:
            response = requests.get(job_url)
            if response.status_code == 200:
                driver1 = response.content
            else:
                print(f"Error getting HTML for {job_url}: {response.status_code}")
            page_content1 = BeautifulSoup(driver1, 'html.parser')
            job_id_element = page_content1.find('div', {'id':"job_reference"})
            job_id = job_id_element.text.replace("Job No:",'').strip() if job_id_element else ''
            job_description_raw = page_content1.find('div', {'id':"job_description"})
            job_description = job_description_raw.text
            job_data.append({
                'Company' : "Water NSW",
                'Job ID' : job_id,
                'Job Title': job_title,
                'Posted date' : posted,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : job_type,
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\waternsw1.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"water nsw complete, runtime: {elapsed_time1:.2f} seconds")
    return count



def vicwater(url, count):
    print('Running vicwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    job_data = []
    driver.get(url)
    time.sleep(3)
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fl-post-content clearfix')))    
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for job_cards in page_content.find_all('div', class_="fl-col-content fl-node-content"):
        if job_cards.find('span', class_="fl-button-text"):
            job_title_element = job_cards.find('div', class_="fl-rich-text")
            job_title1 = job_title_element.span
            if job_title1:
                job_title = job_title1.text.strip() 
            else:
                job_title = job_title_element.h3.text.strip()
            job_url_element = job_cards.find('p', string='Position Description')
            job_url = job_title_element.a['href']
            job_company_element = job_cards.find('div', class_="fl-photo-content fl-photo-img-png")
            if job_company_element is None: job_company_element = job_cards.find('div', class_="fl-photo-content fl-photo-img-jpg")   
            job_company = job_company_element.img['title']
            job_description_raw = job_title_element
            job_description = job_title_element.text.strip()
            job_data.append({
                'Company' : job_company,
                'Job ID' : '',
                'Job Title': job_title,
                'Posted date' : '',
                'URL': job_url,
                'Job Location': '',
                'Work Type' : '',
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : job_description,
                'Job Site' : 'Victoria State Water Jobs'
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\vicwater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"vicwater complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def northeastwater(url, count):
    print('Running northeastwater')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    job_data = []
    driver1 = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for job_card in page_content.find_all('div', class_="content__summary2__row--bg align-items-center"):
        job_title = job_card.h4.text.strip()
        job_url = job_card.a['href']
        try:
            if job_url:
                driver1.get(job_url)
                element = WebDriverWait(driver1, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "content__bar__inner")))
                #WebDriverWait(driver1, 15).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                #time.sleep(5)
                page_content1 = BeautifulSoup(driver1.page_source, 'html.parser').find('div',class_='content__bar__inner')
                count = 0
                for items in page_content1.find_all('div', role = 'tabpanel'):
                    if count == 0:
                        for item in items.find_all('tr'):
                            item1 = item.text.strip()
                            if "Position number" in item1:
                                job_id = item1.replace('Position number\n','')
                            if "Location" in item1:
                                job_location = item1.replace('Location\n','')
                            if "Mandatory Requirements" in item1:
                                job_requirement = []
                                for require in items.find_all('li'):
                                    job_requirement.append(require.text.strip())
                    if count == 1:
                        job_description_raw = items
                        job_description = items.text.strip()
                    if count == 2:
                        for item in items.find_all('li'):
                            job_requirement.append(item.text.strip())
                    count += 1


                job_data.append({
                    'Company' : "North East Water",
                    'Job ID' : job_id,
                    'Job Title': job_title,
                    'Posted date' : '',
                    'URL': job_url,
                    'Job Location': job_location,
                    'Work Type' : '',
                    'Job Categories' : '',
                    'Job Summary' : '',
                    'Job Description Raw' : job_description_raw,
                    'Job Description Text' : job_description,
                    'Job Requirement' : job_requirement
                })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
        except: print('error')

    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\northeastwater.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"northeastwater complete, runtime: {elapsed_time1:.2f} seconds")
    return count


def auscitycouncil(url, count):
    print('Running auscitycouncil')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    job_data = []
    driver.get(url)
    time.sleep(3)
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    working_content = page_content.find('div', class_="wpjb-job-list wpjb-grid")
    for job_cards in working_content.find_all('a'):
        job_url = job_cards['href']
        job_list_details = job_cards.find('div', class_="job-list__details")
        job_title_element = job_list_details.find('div', class_='job-list__title')
        job_title = job_title_element.text.strip() if job_title_element else ''
        job_company_element = job_title_element.find('div', class_="job-list__council")
        job_company = job_company_element.text.strip() if job_company_element else ''
        job_location_element = job_list_details.find('div', class_="job-list__location")
        job_location = job_location_element.text.strip if job_location_element else ''
        job_type_element = job_list_details.find('div', class_="job-list__tag")
        job_type = job_type_element.text.strip() if job_type_element else ''
        posted_date_element = job_cards.find('div', class_="job-list__dates").text.strip().split('Closes:')[0].split(': ')[1]
        if job_url:
            driver1 = webdriver.Chrome()
            driver1.get(job_url)
            page_content = BeautifulSoup(driver1.page_source, 'html.parser')
            working_content = page_content.find('section', class_="section-page-title")
            job_description_element = working_content.find('div',{'itemprop':"description", 'class':"wpjb-job-text"})
            job_description_raw = job_description_element if job_description_element else ''
            #job_description = job_description_element.text.strip()
    
            job_data.append({
                'Company' : job_company,
                'Job ID' : '',
                'Job Title': job_title,
                'Posted date' : posted_date_element,
                'URL': job_url,
                'Job Location': job_location,
                'Work Type' : job_type,
                'Job Categories' : '',
                'Job Summary' : '',
                'Job Description Raw' : job_description_raw,
                'Job Description Text' : '',
                'Job Requirement' : '',
                'Job Site' : 'Australian City Council Jobs'
            })
            print(f'Job {count} pulled for: {job_title}')
            count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\auscitycouncil.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"auscitycouncil complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def wioa(url, count):
    print('Running wioa')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    job_data = []
    driver.get(url)
    time.sleep(15)
    
    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "job_listings")))
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    working_content = page_content.find('ul', class_="job_listings")
    for job_cards in working_content.find_all('li', class_='job_listing'):
        job_id_element = job_cards['class'][0].replace('post-','')
        job_id = job_id_element if job_id_element else ''
        job_url_element = job_cards.a['href']
        job_url = job_url_element if job_url_element else ''
        job_title_element = job_cards.find('div', class_='position')
        job_company_element = job_title_element.find('div', class_="company")
        job_company = job_company_element.text.strip() if job_company_element else ''
        job_title = job_title_element.text.replace(job_company, '').strip() if job_company_element else ''
        job_location_element = job_cards.find('div', class_="location")
        job_location = job_location_element.text.strip() if job_location_element else ''
        posted_element = job_cards.find('li', class_='date')
        posted = posted_element.time['datetime'] if posted_element else ''
        if job_url:
            driver1.get(job_url)
            job_description_element = WebDriverWait(driver1, 15).until( EC.presence_of_element_located((By.CLASS_NAME, "job_description")))
            page_content = BeautifulSoup(driver1.page_source, 'html.parser')
            job_description_element = page_content.find('div', class_="job_description")
            job_description_raw = job_description_element if job_description_element else ''
            job_description = job_description_element.text.strip()
    
        job_data.append({
            'Company' : job_company,
            'Job ID' : job_id,
            'Job Title': job_title,
            'Posted date' : posted,
            'URL': job_url,
            'Job Location': job_location,
            'Work Type' : '',
            'Job Categories' : '',
            'Job Summary' : '',
            'Job Description Raw' : job_description_raw,
            'Job Description Text' : job_description,
            'Job Requirement' : '',
            'Job Site' : 'WIOA'
        })
        print(f'Job {count} pulled for: {job_title}')
        count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\wioa.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"wioa complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def h2o(url, count):
    print('Running h2o')
    start_time1 = time.time()
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    job_data = []
    driver.get(url)
    time.sleep(15)
    page_content = BeautifulSoup(driver.page_source, 'html.parser')
    for job_cards in page_content.find_all('article'):
        job_title_element = job_cards.find('a', class_='link')
        job_title = job_title_element.text.strip() if job_title_element else ''
        if "FEATURED" in job_title:
            job_title_element = job_title.replace('FEATURED','').strip()
            job_title = job_title_element if job_title_element else ''
        job_url = job_cards.a['href'] if job_title_element else ''
        posted_element = job_cards.find('div', class_="listing-item__date")
        posted = posted_element.text.strip() if posted_element else ''
        salary_element = job_cards.find('div', class_="listing-item__info listing-item__info--item-salary-range clearfix")
        salary = salary_element.text.strip() if salary_element else ''
        job_summary_element = job_cards.find('div', class_="listing-item__desc")
        job_summary = job_summary_element.text.strip() if job_summary_element else ''
        job_company_element = job_cards.find('span', class_="listing-item__info--item listing-item__info--item-company")
        job_company = job_company_element.text.strip() if job_company_element else ''
        job_location_element = job_cards.find('span', class_="listing-item__info--item listing-item__info--item-location")
        job_location = job_location_element.text.strip() if job_location_element else ''
        job_type_element = ''
        for items in job_cards.find_all('span', class_="listing-item__info--item listing-item__info--item-employment-type"):
            job_type_element = job_type_element + items.text.strip() + ' '
        job_type = job_type_element.strip() if job_type_element else ''
        if job_url:
            driver1.get(job_url)
            page_content = BeautifulSoup(driver1.page_source, 'html.parser')
            other_element = page_content.find('div', class_="job-type")
            job_category = []
            for items in other_element.find_all('span', class_="job-type__value"):
                job_category.append(items.text.strip())
            job_desc = []
            for items in page_content.find_all('div', class_="details-body__content content-text"):
                job_desc.append(items)
            job_description_raw = job_desc[0] if job_desc[0] else ''
            job_description = job_description_raw.text.strip()
            job_id = job_desc[2].text.strip()
    
        job_data.append({
            'Company' : job_company,
            'Job ID' : job_id,
            'Job Title': job_title,
            'Posted date' : posted,
            'URL': job_url,
            'Job Location': job_location,
            'Work Type' : job_type,
            'Job Categories' : job_category,
            'Job Summary' : job_summary,
            'Job Description Raw' : job_description_raw,
            'Job Description Text' : job_description,
            'Job Requirement' : '',
            'Job Site' : 'H2Oz Water Careers'
        })
        print(f'Job {count} pulled for: {job_title}')
        count += 1
    df = pd.DataFrame(job_data)
    excel_filename = r'C:\Users\User\Desktop\h2o.xlsx'
    df.to_excel(excel_filename, index=False)
    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f'Data saved to {excel_filename}')
    print(f"h2o complete, runtime: {elapsed_time1:.2f} seconds")
    return count

def main():
    count = 1
    url_sunwater = 'https://careers.sunwater.com.au/en/listing/'
    url_goulburn_murray_water = 'https://www.g-mwater.com.au/about/careers/positions-vacant'
    url_seq_water = 'https://careers.seqwater.com.au/cw/en/listing/'
    url_south_east_water = "https://jobs.southeastwater.com.au/search/"
    url_urban_utilities = "https://careers.pageuppeople.com/581/caw/en/listing/"
    url_water_corp = "https://watercorp.taleo.net/careersection/careersection/2/joblist.ftl"
    url_melbourne_water = "https://careers.pageuppeople.com/391/cw/en/listing/"
    url_barwon_water = "https://www.barwonwater.vic.gov.au/about-us/careers"
    url_greater_western_water = "https://careers.gww.com.au/search/?createNewAlert=false&q=&optionsFacetsDD_customfield1="
    url_sa_water = "https://careers.sawater.com.au/caw/en/listing/"
    url_iconwater = "https://recruitment.iconwater.com.au/"
    url_taswater =  "https://taswater.csod.com/ux/ats/careersite/4/home?c=taswater&lang=en-GB"
    url_untiywater = "https://unitywater.careers.site/"
    url_untiywater2 = "https://unitywater.careers.site/?category=&page=2#list"
    url_sydneywater = 'https://talent.sydneywater.com.au/jobs'
    url_hunterwater = "https://hunterwater.csod.com/ux/ats/careersite/1/home?c=hunterwater"
    url_waternsw = "https://www.waternsw.com.au/about-us/working-with-us/careers"
    url_northeastwater = "https://www.newater.com.au/vacancies"
    url_h2o = "https://h2oz.org.au/jobs/"
    url_wioa = "https://wioa.org.au/positions-vacant/"
    url_auscitycouncil = "https://www.careersatcouncil.com.au/jobs/"
    url_vicwater = "https://vicwater.org.au/vic-water-jobs-board/"
    #count = iconwater(url_iconwater, count)
    #count = sunwater(url_sunwater,count)
    #count = goulburn_murray_water(url_goulburn_murray_water, count)
    #count = seq_water(url_seq_water, count)
    #count = south_east_water(url_south_east_water, count)
    #count = urban_utilities(url_urban_utilities, count)
    #count = water_corp(url_water_corp, count)    
    #count = melbourne_water(url_melbourne_water, count)
    #count = barwon_water(url_barwon_water, count)
    #count = greater_western_water(url_greater_western_water, count)
    #count = sa_water(url_sa_water, count)
    #count = taswater(url_taswater,count)
    #count = unitywater(url_untiywater, count)
    #count = unitywater(url_untiywater2, count)
    #count = sydneywater(url_sydneywater, count)
    #count = hunterwater(url_hunterwater, count)
    text = """"""
    count = waternsw(url_waternsw,count,text) #unknown issue with driver, needs to paste html text
    #count = northeastwater(url_northeastwater, count)
    #count = h2o(url_h2o, count)
    #count = wioa(url_wioa, count)
    #count = auscitycouncil(url_auscitycouncil, count)
    #count = vicwater(url_vicwater, count)
    
if __name__ == "__main__":
    print('Starting task')
    start_time = time.time()
    main()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"All task complete, runtime: {elapsed_time:.2f} seconds")
