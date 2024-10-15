import os
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

service = Service("/snap/bin/firefox.geckodriver")

IP=os.environ.get("IP")
PORT=os.environ.get("PORT")

base_url = f"http://{IP}:{PORT}/"

class TestHomePage(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(service=service)
        super(TestHomePage, self).setUp()


    def tearDown(self):
        self.browser.quit()
        super(TestHomePage, self).tearDown()

    def test_create_note_without_login(self):
        browser = self.browser
        browser.get(base_url)

        create_note_button = browser.find_element(By.NAME, "home-button-create-note")
        create_note_button.click()
        
        self.assertEqual(browser.current_url, f"{base_url}note/new/")
        
        page_response = browser.find_element(By.CLASS_NAME, "response")
        
        self.assertEqual(page_response.text, "you have to login first")

    def test_home_page_with_register(self):
        browser = self.browser
        browser.get(base_url)

        register_button = browser.find_element(By.NAME, "register")

        register_button.click()
        self.assertEqual(browser.current_url, f"{base_url}accounts/signup/")

        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys("ehgks")

        password1_input = browser.find_element(By.NAME, "password1")
        password1_input.send_keys("dohadoha")

        password2_input = browser.find_element(By.NAME, "password2")
        password2_input.send_keys("dohadoha")

        password2_input = browser.find_element(By.NAME, "signin")
        password2_input.click()

        logout_button = browser.find_element(By.NAME, "login")

        self.assertEqual(logout_button.text, "login")

    def test_from_home_page_with_login_and_create_note(self):
        browser = self.browser
        browser.get(base_url)

        register_button = browser.find_element(By.NAME, "login")
        register_button.click()

        self.assertEqual(browser.current_url, f"{base_url}accounts/login/")

        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys("hello")

        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys("dohadoha")

        login_button = browser.find_element(By.ID, "login")
        login_button.click()

        logout_button = browser.find_element(By.NAME, "logout")

        self.assertEqual(logout_button.text, "Log Out")

        create_note_button = browser.find_element(By.NAME, "home-button-create-note")
        create_note_button.click()

        message = browser.find_element(By.NAME, "note")
        message.send_keys("message")

        save_button = browser.find_element(By.NAME, "save")
        save_button.click()

        message_url_response = browser.find_element(By.CLASS_NAME, "response")
        url_text = message_url_response.text
        message_url_response.click()

        response_message_return = browser.find_element(By.CLASS_NAME, "response")

        self.assertEqual(response_message_return.text, "message")
        self.assertEqual(browser.current_url, url_text)


    def test_logout_and_create_note_after(self):
        browser = self.browser
        browser.get(base_url)

        register_button = browser.find_element(By.NAME, "login")
        register_button.click()

        self.assertEqual(browser.current_url,f"{base_url}accounts/login/")

        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys("hello")

        password_input = browser.find_element(By.NAME, "password")
        password_input.send_keys("dohadoha")

        login_button = browser.find_element(By.ID, "login")
        login_button.click()

        logout_button = browser.find_element(By.NAME, "logout")
        logout_button.click()

        self.assertEqual(browser.current_url, base_url)
        
        create_note_button = browser.find_element(By.NAME, "home-button-create-note")
        create_note_button.click()
        
        page_response = browser.find_element(By.CLASS_NAME, "response")
        
        self.assertEqual(page_response.text, "you have to login first")




