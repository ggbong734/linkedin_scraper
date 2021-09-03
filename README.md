## LinkedIn Experience Scraper 
_started in August 2021_ 

## Installation 

`python3 -m venv env . env/bin/activate pip3 install --upgrade pip pip3 install -r requirements.txt`

## Testing

TBD

## Description
This program scrapes a LinkedIn profile's relevant years of experience. 

There are two files:
- `scraper.py` has the scraper bot lass
- `run.py` is used to run the program
- The list of relevant titles are in `data/title_index.txt`

Enter the following in `data/constants.py file`:
- Chrome web driver path. Download driver from [here](https://chromedriver.chromium.org/)
- LinkedIn login email address 
- LinkedIn login password 

The output is a dictionary showing the relevant experiences in years.
