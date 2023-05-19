from script.models.report import Report
from config import config

from selenium.webdriver.common.by import By
from selenium import webdriver

from time import sleep

from api.report import report
from api.error import error

class NewsScraper:
    link = config.SITE

    last_report : Report
    temp_report : Report

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def get_last_report(self) -> Report:
        self.driver.get(self.link)
        report = self.driver.find_elements(by=By.CLASS_NAME, value="card-rY32JioV")[0]
        link = report.get_attribute("href")
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
