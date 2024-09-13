import time


from ReadFromFile import arrayFromFile
from selenium.webdriver.common.by import By
from ConfigDriver import driver

# Load Excel data from the sheet
sheet = arrayFromFile()

# ***********************************************************************************************************************************************
# test if the user entre a valid account
def test_rightInputForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(2, 1).value)
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(2, 2).value)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)
    assert      driver.find_element(By.CLASS_NAME ,'woocommerce-MyAccount-content').is_displayed()
# ***********************************************************************************************************************************************

# test if the user entre a valid email but wrong password
def test_WrongPasswordForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(3, 1).value)
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(3, 2).value)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    assert  driver.find_element(By.CLASS_NAME , 'woocommerce').is_displayed() \
            and "incorrect. Lost your password?" in driver.find_element(By.CLASS_NAME , 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
# ***********************************************************************************************************************************************


# test if the user entre a invalid account
def test_WrongEmailForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(4, 1).value)
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(4, 2).value)
    driver.find_element(By.NAME, 'login').click()
    print(driver.find_element(By.CLASS_NAME , 'woocommerce').text)
    time.sleep(3)
    assert  driver.find_element(By.CLASS_NAME , 'woocommerce').is_displayed() \
            and "Unknown email address" in driver.find_element(By.CLASS_NAME , 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
# ***********************************************************************************************************************************************

#test if the password input keep it empty
def test_PasswordInputIsEmptyForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(5, 1).value)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    assert  driver.find_element(By.CLASS_NAME , 'woocommerce').is_displayed() \
            and "The password field is empty." in driver.find_element(By.CLASS_NAME , 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
# ***********************************************************************************************************************************************
# test if the email input keep it empty
def test_EmailInputIsEmptyForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(6, 2).value)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    assert  driver.find_element(By.CLASS_NAME , 'woocommerce').is_displayed()\
            and "Username is required." in driver.find_element(By.CLASS_NAME , 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
# ***********************************************************************************************************************************************

# test if keep all the input(email and password input) empty
def test_AllInputIsEmptyForLogin(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)

    assert  driver.find_element(By.CLASS_NAME , 'woocommerce').is_displayed()\
            and "Username is required." in driver.find_element(By.CLASS_NAME , 'woocommerce-error').find_element(By.TAG_NAME, 'li').text
# ***********************************************************************************************************************************************
# Test if logging in with a valid account and selecting the "remember me" checkbox keeps the account opened after closing and reopening the website
def test_RememberMeButton(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(2, 1).value)
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(2, 2).value)
    driver.find_element(By.ID, 'rememberme').click()
    driver.find_element(By.NAME, 'login').click()
    time.sleep(3)
    driver.close()
    driver.get('http://demostore.supersqa.com')
    driver.find_element(By.LINK_TEXT,'My account').click()

    assert driver.find_element(By.CLASS_NAME ,'woocommerce-MyAccount-content').is_displayed()
# ***********************************************************************************************************************************************
# test if the user entre to "lost password" and entre valid email
def test_LostPasswordWithValidEmail(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.LINK_TEXT, 'Lost your password?').click()
    driver.find_element(By.ID, 'user_login').send_keys(sheet.cell(2, 1).value)
    driver.find_element(By.CSS_SELECTOR, "#post-9 > div > div > form > p:nth-child(4) > button").click()
    assert "Password reset email has been sent." in driver.find_element(By.CLASS_NAME, 'woocommerce-message').text \
    and driver.find_element(By.CLASS_NAME, 'woocommerce-message').is_displayed()
# ***********************************************************************************************************************************************

# test if the user entre to "lost password" and entre invalid email
def test_LostPasswordWithInValidEmail(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.LINK_TEXT, 'Lost your password?').click()
    driver.find_element(By.ID, 'user_login').send_keys(sheet.cell(4, 1).value)
    driver.find_element(By.CSS_SELECTOR, "#post-9 > div > div > form > p:nth-child(4) > button").click()
    assert "Invalid username or email." in driver.find_element(By.CLASS_NAME, 'woocommerce-error').text \
    and driver.find_element(By.CLASS_NAME, 'woocommerce-error').is_displayed()

