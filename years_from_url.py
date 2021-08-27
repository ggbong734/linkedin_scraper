import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# os function to get current directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# direct the webdriver to where the browser file is:

driver_path = r'locaton of driver path' # ENTER PATH to driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# your secret credentials:
email = "your email"  #ENTER your login email
password = "your password"  # ENTER your login password

# Go to linkedin and login
driver.get('https://www.linkedin.com/login')
time.sleep(3)
driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_id('password').send_keys(Keys.RETURN)

url = 'https://www.linkedin.com/in/gerry-bong-71137420/'
url2 = ' https://www.linkedin.com/in/kelseybuckley/'

# Go to the url
driver.get(url)
time.sleep(5)

# Script to scroll to the bottom of the page
SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

pages = 0
while pages < 1:
   # Scroll down to bottom
   driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
   
   # Wait to load page
   time.sleep(SCROLL_PAUSE_TIME)
   
   pages += 1


#class name for each position 
posn_class = "pv-position-entity"

#class name for title in bold like Senior Engineer
ttl_class = "t-16 t-black t-bold"
#class name for title in small bold in sublist
exp_sub_class = "t-14 t-black t-bold"

#class name for experience years
exp_class = "pv-entity__bullet-item-v2"


#positions = driver.find_elements_by_class_name('pv-position-entity')

# Create lists to store each year and title
years_list = []
titles_list = []

# Find each position
titles = driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")

# For each position search for the title and append into the titles_list
for title in titles:
      titles_list.append(title.find_element_by_xpath(".//h3[@class='t-16 t-black t-bold']").text)

# Search all the years of experiences on the page and append into years_list 
exps = driver.find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")
for exp in exps:
   years = 0
   txt = exp.text
   has_years = True if 'yrs' in txt else False
   has_mos = True if 'mos' in txt else False
   if has_years and has_mos:
         years = int(txt[0]) + int(txt[6])/12
   elif has_mos and not has_years:
         years = int(txt[0])/12
   elif not has_mos and has_years:
         years = int(txt[0])
   years_list.append(round(years,2))

total_years = sum(years_list)
   
print("The total experience of the person is:{0} years".format(total_years))

i = 1
for title, year in zip(titles_list, years_list):
   print ("The {0} most recent position this person held was {1} for {2} years".format(i, title, year))
   i += 1

# Create a dictionary for the output
d = {"total_years_experience": 0}
d["specialties"] = []
total_years_in_idx = 0

# open a local text file with all the index titles and parse a list
with open(os.path.join(__location__,'title_index.txt'),'r') as index_file:
    title_idx_list = index_file.read().splitlines()  

# Loop through the title list and match the years to the titles
for i in range(min(len(titles_list), len(years_list))):
   if titles_list[i] in title_idx_list:
         d["specialties"].append({"Name":titles_list[i], "Type_c":"Specialty" ,"Amount": years_list[i]})
         total_years_in_idx += years_list[i]  

# Add the total relevant experiences into the dictionary
d["total_years_experience"]= total_years_in_idx

print(d)

close browser
driver.close()

# Reference: https://medium.com/nerd-for-tech/linked-in-web-scraper-using-selenium-15189959b3ba
# Reference: https://levelup.gitconnected.com/linkedin-scrapper-a3e6790099b5