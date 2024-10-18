import asyncio
import random
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import os

load_dotenv()


async def cappa_register(user_data):
    """
    Registers a new user on CAPPA.

    Parameters
    ----------
    username : str
        The desired username for the new user.
    email : str
        The desired email for the new user.
    password : str
        The desired password for the new user.
    first_name : str, optional
        The desired first name for the new user. Defaults to "FirstName".
    last_name : str, optional
        The desired last name for the new user. Defaults to "LastName".
    """
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(os.getenv("REGISTRATION_URL"))
    await asyncio.sleep(5)

    fields = {
        "id_username": user_data["username"],
        "id_email": user_data["email"],
        "id_first_name": user_data["username"],
        "id_last_name": user_data["username"],
        "id_password1": user_data["password"],
        "id_password2": user_data["password"],
    }

    for field_id, value in fields.items():
        field = browser.find_element(By.ID, field_id)
        field.send_keys(value)

    continue_button = browser.find_element(
        By.XPATH, value="/html/body/div[1]/main/div/div[2]/div/form/input[3]"
    )
    continue_button.click()
    await asyncio.sleep(5)

    assert browser.title == "CAPPA"
    await asyncio.sleep(5)

    # browser.quit()


async def cappa_login(username, password):
    """
    Logs in to CAPPA with the given credentials.

    Parameters
    ----------
    username : str
        The username to log in with.
    password : str
        The password to log in with.
    """
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(os.getenv("LOGIN_URL"))
    await asyncio.sleep(5)
    browser.find_element(By.ID, "id_login").send_keys(username)
    browser.find_element(By.ID, "id_password").send_keys(password)
    login_button = browser.find_element(
        By.XPATH, "/html/body/div[1]/main/div/div[2]/div/form/input[5]"
    )
    login_button.click()
    await asyncio.sleep(5)
    assert browser.title == "CAPPA"
    await asyncio.sleep(5)
