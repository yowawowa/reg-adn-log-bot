import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()


def register(username, email, password, first_name="FirstName", last_name="LastName"):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(os.getenv("REGISTRATION_URL"))
    time.sleep(5)

    fields = {
        "id_username": username,
        "id_email": email,
        "id_first_name": first_name,
        "id_last_name": last_name,
        "id_password1": password,
        "id_password2": password,
    }

    for field_id, value in fields.items():
        field = browser.find_element(By.ID, field_id)
        field.send_keys(value)

    continue_button = browser.find_element(
        By.XPATH, value="/html/body/div[1]/main/div/div[2]/div/form/input[3]"
    )
    continue_button.click()
    time.sleep(5)

    assert browser.title == "CAPPA"
    time.sleep(5)

    # browser.quit()


def login(username, password):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(os.getenv("LOGIN_URL"))
    time.sleep(5)
    browser.find_element(By.ID, "id_login").send_keys(username)
    browser.find_element(By.ID, "id_password").send_keys(password)
    login_button = browser.find_element(By.XPATH, "//input[@value='Login']")
    login_button.click()
    time.sleep(5)
    assert browser.title == "CAPPA"
    time.sleep(5)