from script.models.report import Report
from config import config

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from time import sleep

from api.report import report
from api.error import error

class NewsScraper:
    link = config.SITE

    last_report : Report = None
    temp_report : Report = None

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    def __init__(self) -> None:
        self.path = None if config.CRHOME_DRIVER == "" else config.CRHOME_DRIVER
        self.driver = self.new_driver()

    def new_driver(self) -> webdriver.Chrome:
        

        return webdriver.Chrome(
            self.path, 
            chrome_options=self.chrome_options
        )

    def get_last_report(self) -> Report:
        self.driver.get(self.link)
        report = self.driver.find_element(by=By.CLASS_NAME, value="largeTitle").find_elements(by=By.TAG_NAME, value="article")[0]
        link = report.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        title = report.text

        return Report(title, link)

    @property
    def is_new(self) -> bool:
        if self.last_report != self.temp_report:
            self.last_report = self.temp_report
            return True
        else:
            return False
        

    def connect_news(self):
        while True:
            try:
                self.temp_report = self.get_last_report()
            except Exception as e:
                error(e)
                try:
                    self.driver.quit()
                    self.driver = webdriver.Chrome()
                except Exception as e:
                    error(e)
            else:
                if self.is_new:
                    report(self.last_report)
            sleep(60)
