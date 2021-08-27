import time
import logging
import os 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver_path = r'D:/Python_project/chromedriver.exe'

#current directory
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class LinkedInExperienceScraperBot:
    def __init__(self, delay=5):
        if not os.path.exists("data"):
            os.makedirs("data")
        # Log format
        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt)
        self.delay=delay
        # Set up options
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Start driver
        logging.info("Starting driver")
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    def log_in(self, email, password):
        """Log in to LinkedIn to enable access to user profile
        """
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(3)
        self.driver.find_element_by_id('username').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password').send_keys(Keys.RETURN)

    def load_url(self, url):
        """Visit the url and wait for page to load
        """
        self.driver.get(url)
        time.sleep(5)

    def scroll_to_half(self):
        """Scroll to half of the document body to load the years of experience
        LinkedIn only displays the data when user is on the experience page
        """
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        pages = 0
        while pages < 1:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.5);")
        
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            pages += 1

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page to load years of experience
        """
        SCROLL_PAUSE_TIME = 3
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def extract_total_experience(self):
        """Extract experience data in years and titles and compile into a dictionary
        """
        # get a list of all the years of experience 
        # list_positions = self.driver.find_elements_by_class_name('pv-position-entity')
        # list_exps = driver.find_elements_by_class_name('pv-entity__bullet-item-v2')
        
        # Create lists to store each year and title
        years_list = []
        titles_list = []

        # Find each position
        titles = self.driver.find_elements_by_xpath("//a[@data-control-name='background_details_company']")

        # For each position search for the title and append into the titles_list
        for title in titles:
            titles_list.append(title.find_element_by_xpath(".//h3[@class='t-16 t-black t-bold']").text)

        # Search all the years of experiences on the page and append into years_list 
        exps = self.driver.find_elements_by_xpath("//span[@class='pv-entity__bullet-item-v2']")
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

        total_years_all = sum(years_list)

        # Create a dictionary for the output
        d ={"total_years_experience": 0}
        d["specialties"] = []
        total_years_in_idx = 0
        
        # Open a local file with the list of titles to search for
        with open(os.path.join(__location__,'title_index.txt'),'r') as index_file:
            title_idx_list = index_file.read().splitlines()  

        # Loop through the title list and match the years to the titles
        for i in range(min(len(titles_list), len(years_list))):
            if titles_list[i] in title_idx_list:
                d["specialties"].append({"Name":titles_list[i], "Type_c":"Specialty", "Amount": years_list[i]})
                total_years_in_idx += years_list[i]  

        # Add the total relevant experiences into the dictionary
        d["total_years_experience"]= total_years_in_idx

        return d

    def close_session(self):
        """This function closes the actual session"""
        logging.info("Closing session")
        self.driver.close()

    def run(self, email, password, url):
        """Function to run the bot and return the experience dictionary
        """
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(3)
        logging.info("Logging in")

        self.login(
                email=email,
                password=password
            )
        logging.info("Begin candidate profile search")
        self.load_url(url)
        self.scroll_to_half()
        result = self.extract_total_experience()

        #close browser
        logging.info("Done scraping.")
        logging.info("Closing DB connection.")

        bot.close_session()
        return result

if __name__ == "__main__":
    email = "your email"
    password = "your password"
    url="candidate url"
    bot = LinkedInExperienceScraperBot()
    bot.run(email, password)