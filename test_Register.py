import time


from ReadFromFile import arrayFromFile
from selenium.webdriver.common.by import By
from ConfigDriver import driver

# Load Excel data from the sheet
sheet = arrayFromFile()
# ***********************************************************************************************************************************************
# test if register by account unused
def test_rightInputForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_email').send_keys(sheet.cell(9, 1).value)
    driver.find_element(By.ID, 'reg_password').send_keys(sheet.cell(9, 2).value)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)
    assert      driver.find_element(By.CLASS_NAME ,'woocommerce-MyAccount-content').is_displayed()
# ***********************************************************************************************************************************************
# test if register by account used
def test_EmailAlreadyUsedForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_email').send_keys(sheet.cell(10, 1).value)
    driver.find_element(By.ID, 'reg_password').send_keys(sheet.cell(10, 2).value)
    time.sleep(3)
    assert     not  driver.find_element(By.NAME, 'register').is_enabled()
# ***********************************************************************************************************************************************
# test if register with unused email but the password not applies the policy
def test_PasswordNotAppliesPolicyForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_email').send_keys(sheet.cell(12, 1).value)
    driver.find_element(By.ID, 'reg_password').send_keys(sheet.cell(12, 2).value)
    time.sleep(3)
    assert     not  driver.find_element(By.NAME, 'register').is_enabled()
# ***********************************************************************************************************************************************
# test if keep the email input empty
def test_EmailInputEmptyForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_password').send_keys(sheet.cell(13, 2).value)
    time.sleep(3)
    assert     not  driver.find_element(By.NAME, 'register').is_enabled()
# ***********************************************************************************************************************************************
# test if keep the password input empty
def test_PasswordInputEmptyForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_email').send_keys(sheet.cell(14, 1).value)
    time.sleep(3)
    assert     not  driver.find_element(By.NAME, 'register').is_enabled()
# ***********************************************************************************************************************************************

# test if keep all the input empty ( email and password input)
def test_AllInputEmptyForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    assert     not  driver.find_element(By.NAME, 'register').is_enabled()
# ***********************************************************************************************************************************************

# test if entre an email not applies the email form correctly
def test_EmailNotAppliesTheEmailFormForRegister(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.ID, 'reg_email').send_keys(sheet.cell(11, 1).value)
    driver.find_element(By.ID, 'reg_password').send_keys(sheet.cell(11, 2).value)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)
    assert      driver.find_element(By.CLASS_NAME ,'required').is_displayed()
# ***********************************************************************************************************************************************
# test if the "Privacy Policy" link work (open the Privacy Policy page)
def test_PrivacyPolicyLink(driver):
    driver.get('http://demostore.supersqa.com/my-account/')
    driver.find_element(By.LINK_TEXT, 'privacy policy').click()

    assert driver.find_element(By.CLASS_NAME ,'page-title').text != 'Oops! That page can’t be found.'

