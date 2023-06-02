from script.models.report import Report
from config import config

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from time import sleep

from api.telegram.report import report
from api.telegram.error import error

from helpers.error import restart_on_crash


class NewsScraper:
    link = config.SITE

    last_report: Report = Report(None, None)
    temp_report: Report = Report(None, None)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    def __init__(self) -> None:
        self.path = None if config.CRHOME_DRIVER == "" else config.CRHOME_DRIVER
        self.driver = self.new_driver()

    def new_driver(self) -> webdriver.Chrome:
        if self.path:
            return webdriver.Chrome(
                self.path,
                chrome_options=self.chrome_options
            )

        else:
            return webdriver.Chrome()

    def get_last_content(self) -> str:
        ...

    def get_last_report(self) -> Report:
        ...

    @property
    def is_new(self) -> bool:
        if self.last_report.link != self.temp_report.link:
            self.last_report = self.temp_report
            return True
        else:
            return False

    @restart_on_crash(forever=True)
    def connect_news(self):
        while True:
            try:
                self.temp_report = self.get_last_report()
            except Exception as e:
                error(e)
                self.driver.quit()
                self.driver = self.new_driver()

            else:
                if self.is_new:
                    self.last_report.content = self.get_last_content()
                    report(self.last_report)
            sleep(60)
