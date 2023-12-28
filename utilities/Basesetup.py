import inspect

import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.usefixtures("setup")
class basesetup:

    def base_url(self):
        self.driver.get("https://rahulshettyacademy.com/seleniumPractise/")
        self.driver.implicitly_wait(5)

    def verify_the_element(self,element_to_verify):
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.presence_of_element_located(element_to_verify))

    def getLogger(self):
        name = inspect.stack()[1][3]
        logger = logging.getLogger(name)
        filehandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter('%(asctime)s :%(levelname)s : %(name)s: %(message)s')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        logger.setLevel(logging.DEBUG)
        return logger
