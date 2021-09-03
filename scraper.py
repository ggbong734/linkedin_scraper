from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import data.constants as const
import logging
import os 

#current directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class LinkedInExperienceScraperBot(webdriver.Chrome):
    def __init__(self, driver_path = const.CHROME_WEBDRIVER_PATH,
                teardown=False): 
        self.driver_path = driver_path 
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(LinkedInExperienceScraperBot, self).__init__(self.driver_path, options=options)
        self.implicitly_wait(3)
        self.maximize_window()

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        logging.info("Starting Selenium Chrome driver")

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("Done scraping.")
        if self.teardown:
            logging.info("Closing browser.")
            self.quit()

    def log_in(self, email, password):
        """Log in to LinkedIn to enable access to user profile
        """
        self.get(const.LINKED_IN_LOGIN_URL)
        self.implicitly_wait(3)
        self.find_element_by_id('username').send_keys(email)
        self.find_element_by_id('password').send_keys(password)
        self.find_element_by_id('password').send_keys(Keys.RETURN)
        logging.info("Logging in")

    def load_url(self, url):
        """Visit the url and wait for page to load
        """
        self.get(url)
        logging.info("Loading candidate url page")
        self.implicitly_wait(5)

    def scroll_down(self):
        """Press the down key five times many times 
        """
        SCROLL_PAUSE_TIME = 3

        for _ in range(4):
            self.find_element_by_css_selector('body').send_keys(Keys.SPACE)
            self.implicitly_wait(SCROLL_PAUSE_TIME)

    def click_more_exp(self):
        """Click on the more experience button if candidate has a lot of experience
        """
        try: 
            exp_button = self.find_element_by_xpath("//button[contains(text(), 'more experience')]")
            exp_button.click()
        except:
            logging.info("No expand experience button found. Skipping..")
        
    def extract_total_experience(self):
        """Extract experience data in years and titles and compile into a dictionary
           REF
           https://www.youtube.com/watch?v=j7VZsCCnptM&t=7603s
        """
        # Create lists to store each year and title
        years_list = []
        titles_list = []

        # Find each position
        #titles = self.find_elements_by_xpath("//a[@data-control-name='background_details_company']")
        titles = self.find_elements_by_xpath("//li[@class='pv-entity__position-group-pager pv-profile-section__list-item ember-view']")       

        # For each position search for the title and append into the titles_list
        for title in titles:
            try:
                #subtitles = title.find_elements_by_xpath(".//span[@class='t-14 t-black t-bold']").text
                subtitles = title.find_elements_by_xpath(".//h3[@class='t-14 t-black t-bold']")
                if len(subtitles) >= 2:
                    for subtitle in subtitles:
                        subtitle_text = subtitle.find_element_by_xpath(".//span[not(@class = 'visually-hidden')]").text
                        titles_list.append(subtitle_text)
                else:
                    titles_list.append(title.find_element_by_xpath(".//h3[@class='t-16 t-black t-bold']").text)

            except:
                logging.info("subtitles not found")

        # Search all the years of experiences on the page and append into years_list 
        exps = self.find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")
        for exp in exps:
            years = 0
            txt = exp.text.replace('s','')

            has_years = True if 'yr' in txt else False
            has_mos = True if 'mo' in txt else False
            if has_years and has_mos:
                    splt_txt = txt.split('yr')
                    years = int(splt_txt[0]) + int(splt_txt[1].replace(' mo', ''))/12
            elif has_mos and not has_years:
                    years = int(txt.split(' mo')[0])/12
            elif not has_mos and has_years:
                    years = int(txt.split(' yr')[0])
            years_list.append(round(years,2))

        total_years_all = sum(years_list)
        print("List of experiences in years:", years_list)
        print("Past job titles:", titles_list)

        # Create a dictionary for the output
        d ={"total_years_experience": 0}
        d["specialties"] = []
        total_years_in_idx = 0
        
        # Open a local file with the list of titles to search for
        with open(os.path.join(__location__,'data/title_index.txt'),'r') as index_file:
            title_idx_list = index_file.read().splitlines()  

        # Loop through the title list and match the years to the titles
        for i in range(min(len(titles_list), len(years_list))):
            if titles_list[i] in title_idx_list:
                d["specialties"].append({"Name":titles_list[i], "Type_c":"Specialty", "Amount": years_list[i]})
                total_years_in_idx += years_list[i]  

        # Add the total relevant experiences into the dictionary
        d["total_years_experience"]= total_years_in_idx

        return d

