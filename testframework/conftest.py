import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope='class')
def setup(request):
    service_obj = Service("C:/Users/Chandru/Documents/chromedriver.exe")
    driver = webdriver.Chrome(service=service_obj)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.minimize_window()
    driver.close()