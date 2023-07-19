from script.models.report import Report
from config import config

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from time import sleep

from api.telegram.report import report
from api.telegram.error import error
from api.wordpress.send_report import send_report
from api.telegram.connection import send_message

from helpers.error import restart_on_crash

import re


class NewsScraper:
    link = config.SITE

    last_report: Report = {"link": None}
    temp_report: Report = {"link": None}

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

    def login(self):
        self.driver.get("https://customer.armut.com/login")
        # wait to load page
        self.driver.implicitly_wait(10)

        username = self.driver.find_element(
            By.XPATH, "/html/body/app-root/cusapp-login-header/cusapp-login-page/form/div/input")
        username.send_keys(config.ARMUT_USERNAME)

        password = self.driver.find_element(
            By.XPATH, "/html/body/app-root/cusapp-login-header/cusapp-login-page/form/div/div[2]/input")
        password.send_keys(config.ARMUT_PASSWORD)

        login_button = self.driver.find_element(
            By.XPATH, "/html/body/app-root/cusapp-login-header/cusapp-login-page/form/div/button")
        login_button.click()

        self.driver.implicitly_wait(10)
        sleep(3)

    def get_last_content(self) -> str:
        self.driver.get(self.last_report.link)

    def get_last_report(self) -> Report:
        self.driver.get(self.link)
        self.driver.implicitly_wait(10)
        sleep(10)

        last_opportunity = self.driver.find_element(
            by="xpath",
            value="/html/body/app-root/app-container/proapp-dashboard/div/div[1]/div/proapp-opportunity-card[1]/div"
        )

        text = last_opportunity.text
        last_opportunity.click()

        return {
            "owner": text.split('\n')[0],
            "title": text.split('\n')[1].split('-')[0].strip(),
            "location": re.search(r'-(.*?)-', text).group(1).strip(),
            "count": text.split('\n')[-1].split('-')[-1].strip(),
            "content": text.split('\n')[-2].split('-')[-1].strip(),
            "link": self.driver.current_url
        }

    @property
    def is_new(self) -> bool:
        if self.last_report["link"] != self.temp_report["link"]:
            self.last_report = self.temp_report
            return True
        else:
            return False

    # @restart_on_crash(forever=True, max_attempts=1)
    def connect_news(self):
        self.login()
        while True:
            try:
                self.temp_report = self.get_last_report()
            except Exception as e:
                error(e)
                self.driver.quit()
                self.driver = self.new_driver()
                self.login()

            else:
                try:
                    if self.is_new:
                        send_message(str(self.last_report))
                except:
                    pass

            self.get_last_report()
            sleep(5)
