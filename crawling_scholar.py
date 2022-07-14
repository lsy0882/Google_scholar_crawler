import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
import time
import random
import subprocess
import shutil

parameters = {
    'chromedriver_path' : 'C:/Users/lsy/local_code/Google_scholar_crawler/chromedriver.exe',
    'keyword' : 'IEEE/CVF International Conference',
    'end_page' : 90,
    'from_year' : 2022,
    'result_folder_name' : 'data',
    'excel_name' : 'IEEE_CVF.xlsx',
    'sheet_name' : 'test'
}


remove_words = ["[HTML] ", "[PDF] "]
def preprocess_title(input_str):
    for remove_word in remove_words:
        input_str = input_str.replace(remove_word, '')
    return input_str

def preprocess_title_info(input_str):
    input_str_list = input_str.split(" ")
    if len(input_str_list) <= 2:
        quote_num = 0
    else:
        if "회" in input_str_list[2]:
            quote_num = int(input_str_list[2].replace("회",""))
        else:
            quote_num = 0
    return quote_num

def preprocess_year_authors(input_str, mode): # mode : [first_author, journal, year, publisher]
    input_str_split = input_str.split("-")
    authors = input_str_split[0]
    journal_year = input_str_split[-2].split(",")
    publisher = input_str_split[-1]

    first_author = authors.split(",")[0]
    if len(journal_year) == 2:
        journal = journal_year[0].strip()
        year = journal_year[1].strip()
    else:
        journal = "None"
        year = journal_year[0].strip()
    publisher = publisher.strip()
    
    if mode == "first_author":
        return first_author
    elif mode == "journal":
        return journal
    elif mode == "year":
        return year
    elif mode == "publisher":
        return publisher

# Run Chrome debugger mode for avoiding reCAPTCHA
try:
    shutil.rmtree(r"c:\chrometemp")  # Remove cookies and cache files
except FileNotFoundError:
    pass
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(parameters['chromedriver_path'], options=option) # Set chromedriver in your .py path!
driver.implicitly_wait(10)

url = "https://scholar.google.com/"
driver.get(url)
time.sleep(random.randint(15, 30))

# driver.find_element_by_name(<element의 name>).send_keys(<검색어>)
element = driver.find_element('name','q')
keyword = parameters['keyword'] # My favorite keyword! : "IEEE/CVF Conference on Computer Vision and Pattern Recognition International Conference on Learning Representations"
element.send_keys(keyword)
time.sleep(random.randint(20, 40))

#perform Google search with Keys.ENTER
element.send_keys(Keys.ENTER)
time.sleep(random.randint(30, 50))

start_time = time.time()
total_titles = []
total_quotes = []
total_first_authors = []
total_journals = []
total_years = []
total_publishers = []
pages = [number for number in range(parameters['end_page'])]
# random.shuffle(pages)
searching_page_num = len(pages)

# crawl one page end
keyword_replace = keyword.replace(" ", "+")
from_year = parameters['from_year']
count = 0
print("Crawling start!")
print("Crawling Info : \n keyword : {0} \n from_year : {1} \n searching page number : {2}".format(keyword, from_year, searching_page_num))
for page in pages:
    count += 1
    element = driver.get("https://scholar.google.co.kr/scholar?start={0}&q={1}&hl=ko&as_sdt=0,5&&as_ylo={2}".format(page*10, keyword_replace, from_year))
    time.sleep(random.randint(60, 80))
    
    title_intance_list = driver.find_elements(By.CLASS_NAME, 'gs_rt')
    title_info_instance_list = driver.find_elements(By.CLASS_NAME, 'gs_fl')
    authors_year_pusblisher_instance_list = driver.find_elements(By.CLASS_NAME, 'gs_a')
    time.sleep(random.randint(40, 50))

    current_titles = [preprocess_title(title_instance.accessible_name) for title_instance in title_intance_list]
    current_quotes = [preprocess_title_info(title_info_instance.text) for title_info_instance in title_info_instance_list if "저장" in title_info_instance.text]
    current_first_authors = [preprocess_year_authors(authors_year_pusblisher_instance.text, "first_author") for authors_year_pusblisher_instance in authors_year_pusblisher_instance_list]
    current_journals = [preprocess_year_authors(authors_year_pusblisher_instance.text, "journal") for authors_year_pusblisher_instance in authors_year_pusblisher_instance_list]
    current_years = [preprocess_year_authors(authors_year_pusblisher_instance.text, "year") for authors_year_pusblisher_instance in authors_year_pusblisher_instance_list]
    current_publishers = [preprocess_year_authors(authors_year_pusblisher_instance.text, "publisher") for authors_year_pusblisher_instance in authors_year_pusblisher_instance_list]
    time.sleep(random.randint(30, 40))

    total_titles.extend(current_titles)
    total_quotes.extend(current_quotes)
    total_first_authors.extend(current_first_authors)
    total_journals.extend(current_journals)
    total_years.extend(current_years)
    total_publishers.extend(current_publishers)
    time.sleep(random.randint(60, 80))

    print("Crawling progresss = {0:03d} page / {1:03d} pages".format(count, searching_page_num))

summary_dataframe = pd.DataFrame({
    'year' : total_years,
    'journal' : total_journals,
    'first_author' : total_first_authors,
    'title' : total_titles,
    'quote' : total_quotes,
    'publisher' : total_publishers
})

# Save dataframe to excel file
base = os.path.dirname(os.path.abspath(__file__))
result_folder_name = parameters['result_folder_name']
excel_name = parameters['excel_name']
sheet_name_cumstom = parameters['sheet_name']
with pd.ExcelWriter(os.path.join(base, result_folder_name, excel_name)) as excel_writer:
    summary_dataframe.to_excel(excel_writer, sheet_name = sheet_name_cumstom)

# Summary progress results
finish_time = time.time()
print("Crawling finish.")
print("TimeSpent : {0} sec".format(round(finish_time-start_time, 2)))
print("Excel file is stored in {0}".format(os.path.join(base, result_folder_name, excel_name)))
print()