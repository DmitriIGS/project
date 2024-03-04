import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

@pytest.fixture(scope="module")
def chrome_options():
    options = Options()
    options.add_experimental_option("detach", True)
    return options


@pytest.fixture(scope="module")
def browser(chrome_options):
    chrome_driver = webdriver.Chrome(chrome_options)
    chrome_driver.maximize_window()
    chrome_driver.implicitly_wait(10)
    yield chrome_driver


@pytest.fixture(scope="module")
def rand_number_for_entites():
    rand_number = str(random.randint(100000, 999999))
    return rand_number