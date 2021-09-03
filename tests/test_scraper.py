from scraper import LinkedInExperienceScraperBot
import data.constants as const

def test_scrape_courtney_wong_url():
    with LinkedInExperienceScraperBot() as bot:
        bot.log_in(email=const.LOGIN_EMAIL, password=const.LOGIN_PASSWORD)
        bot.load_url(const.URL_COURTNEY_WONG)
        bot.scroll_down()
        bot.click_more_exp()
        result = bot.extract_total_experience()
        print(result)
        assert result == {'total_years_experience':3.17,
                        'specialties':[{'Name':
                            'Software Engineer',
                            'Type_c': 'Specialty',
                            'Amount': 3.17}]}




