from scraper import LinkedInExperienceScraperBot
import data.constants as const

with LinkedInExperienceScraperBot() as bot:
    bot.log_in(email=const.LOGIN_EMAIL, password=const.LOGIN_PASSWORD)
    bot.load_url(const.URL_COURTNEY_WONG)
    bot.scroll_down()
    bot.click_more_exp()
    result = bot.extract_total_experience()
    print(result)
