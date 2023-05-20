from script.models.report import Report
from config import config

from selenium.webdriver.common.by import By
from selenium import webdriver

from time import sleep

from api.report import report
from api.error import error

class NewsScraper:
    link = config.SITE

    last_report : Report = None
    temp_report : Report = None

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

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
