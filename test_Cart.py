import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from ReadFromFile import arrayFromFile
from ConfigDriver import driver

# Load Excel data from the sheet
sheet = arrayFromFile()


# ***********************************************************************************************************************************************
# test if the cart was empty and the user entre to cart page it will show message "Your cart is currently empty."
def test_CartIsEmpty(driver):
    driver.get("http://demostore.supersqa.com/cart/")
    assert driver.find_element(By.CLASS_NAME, "cart-empty").is_displayed() \
           and 'Your cart is currently empty.' in driver.find_element(By.CLASS_NAME, "cart-empty").text


# ***********************************************************************************************************************************************
# test if the "Return to shop" button will return you to home page
def test_ReturnToShop_Button(driver):
    driver.get("http://demostore.supersqa.com/cart/")
    driver.find_element(By.LINK_TEXT, 'Return to shop').click()
    assert driver.current_url == 'http://demostore.supersqa.com/'


# ***********************************************************************************************************************************************

def test_Add2ItemToCart(driver):
    # add 2 item in the cart and go to cart page
    driver.get("http://demostore.supersqa.com")

    # get the name of the items that the user add it to check its add the correct item
    ItemName1 = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__title')[0].text
    ItemName2 = driver.find_elements(By.CLASS_NAME, 'woocommerce-loop-product__title')[1].text
    Add2ItemToCart(driver)

    # get the total price for all items in the tabel
    rows_shop_table = driver.find_element(By.CSS_SELECTOR, "#post-7 > div > div > form > table > tbody").find_elements(
        By.TAG_NAME, "tr")
    price = TotalPriceCalculate(driver, rows_shop_table)

    # get the total price that shown in the Cart totals
    rows_cart_totals = driver.find_element(By.CSS_SELECTOR,
                                           "#post-7 > div > div > div.cart-collaterals > div > table > tbody").find_elements(
        By.TAG_NAME, "td")

    # check if the first item successfully added to cart
    # and   check if the second item successfully added to cart
    # and   check if the total of the items in the Shop table is equal the price that shown in the total Cart
    assert ItemName1 in GetItemNameFromShopCartTable(driver, 0, rows_shop_table) \
           and ItemName2 in GetItemNameFromShopCartTable(driver, 1, rows_shop_table) \
           and price == float(rows_cart_totals[0].text.replace('$', ''))


# ***********************************************************************************************************************************************


def test_Remove1ItemFromCart(driver):
    # add 2 item in the cart and go to cart page
    driver.get("http://demostore.supersqa.com")
    Add2ItemToCart(driver)

    # get the total price for all items in the tabel before Remove the first item
    rows_shop_table = driver.find_element(By.CSS_SELECTOR, "#post-7 > div > div > form > table > tbody").find_elements(
        By.TAG_NAME, "tr")
    ItemName = GetItemNameFromShopCartTable(driver, 0, rows_shop_table)

    TotalPriceBeforeRemove = TotalPriceCalculate(driver, rows_shop_table)

    # get the price of the element that we need to Remove and then Remove it
    ItemPrice = float(rows_shop_table[0].find_elements(By.TAG_NAME, "td")[3].text.replace('$', ''))
    rows_shop_table[0].find_element(By.TAG_NAME, "a").click()
    time.sleep(3)

    # get the total price for all items in the tabel after Remove the first item
    rows_shop_table = driver.find_element(By.CSS_SELECTOR, "#post-7 > div > div > form > table > tbody").find_elements(
        By.TAG_NAME, "tr")
    TotalPriceAfterRemove = TotalPriceCalculate(driver, rows_shop_table)

    # get the total price that shown in the Cart totals
    rows_cart_totals = driver.find_element(By.CSS_SELECTOR,
                                           "#post-7 > div > div > div.cart-collaterals > div > table > tbody") \
        .find_elements(By.TAG_NAME, "td")

    # check if the item removed
    # and   check if the total price after remove it equal (the total price before remove it - the price of the item that removed
    # and     check if the total of the items in the Shop table is equal the price that shown in the total Cart
    assert ItemName not in rows_shop_table[0].find_elements(By.TAG_NAME, "td")[2].text \
           and TotalPriceAfterRemove == (TotalPriceBeforeRemove - ItemPrice) \
           and float(rows_cart_totals[0].text.replace('$', '')) == TotalPriceAfterRemove


# ***********************************************************************************************************************************************

# calculate the whole price in the Shop Cart table
def TotalPriceCalculate(driver, rows_shop_table):
    total = 0
    for i in range(len(rows_shop_table) - 1):
        total += float(rows_shop_table[i].find_elements(By.TAG_NAME, "td")[5].text.replace('$', ''))
    return total


# ***********************************************************************************************************************************************

# add 2 item in the cart and go to cart page
def Add2ItemToCart(driver):
    driver.find_element(By.XPATH, '//*[@id="main"]/ul/li[1]/a[2]').click()
    driver.find_element(By.XPATH, '//*[@id="main"]/ul/li[2]/a[2]').click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/ul/li[1]/a[3]')))
    driver.find_element(By.XPATH, '//*[@id="main"]/ul/li[1]/a[3]').click()


# ***********************************************************************************************************************************************

# entre to account in the website
def LoginToAccount(driver):
    driver.get('http://demostore.supersqa.com/my-account/')

    driver.find_element(By.NAME, 'username').send_keys(sheet.cell(2, 1).value)
    driver.find_element(By.NAME, 'password').send_keys(sheet.cell(2, 2).value)
    driver.find_element(By.NAME, 'login').click()

    driver.find_element(By.LINK_TEXT, 'Home').click()


# ***********************************************************************************************************************************************
# get the name of the item in the shop table by index of row
def GetItemNameFromShopCartTable(driver, RowNumber, rows_shop_table):
    return rows_shop_table[RowNumber].find_elements(By.TAG_NAME, "td")[2].text


# ***********************************************************************************************************************************************

# test if the user login then  add items to cart the items will be saved even if log out
def test_ItemsSavedInCartForAccount(driver):
    # login to account
    LoginToAccount(driver)

    # add 2 item in the cart and go to cart page
    Add2ItemToCart(driver)

    # get the items that add to cart from shop table before logout from account
    rows_shop_table = driver.find_element(By.XPATH, '//*[@id="post-7"]/div/div/form/table/tbody').find_elements(
        By.TAG_NAME, "tr")
    itemsBeforeLogout = [cell.text for row in rows_shop_table for cell in row.find_elements(By.TAG_NAME, "td")]

    # logging out from the account
    driver.find_element(By.LINK_TEXT, 'My account').click()
    driver.find_element(By.LINK_TEXT, 'Logout').click()

    # log in again
    LoginToAccount(driver)

    # get the items that add to cart from shop table after logout from account
    driver.find_element(By.LINK_TEXT, 'Cart').click()
    rows_shop_table = driver.find_element(By.XPATH, '//*[@id="post-7"]/div/div/form/table/tbody').find_elements(
        By.TAG_NAME, "tr")
    itemsAfterLogout = [cell.text for row in rows_shop_table for cell in row.find_elements(By.TAG_NAME, "td")]

    # check if the items still in the cart (if the items before logout is like the items after )
    assert itemsBeforeLogout == itemsAfterLogout


# ***********************************************************************************************************************************************

# test if the links of the items page in the shop table is work
def test_OpenItemPage(driver):
    driver.get('http://demostore.supersqa.com')

    # add 2 item in the cart and go to cart page
    Add2ItemToCart(driver)

    # click the link in the table and get name of item
    rows_shop_table = driver.find_element(By.XPATH, '//*[@id="post-7"]/div/div/form/table/tbody').find_elements(
        By.TAG_NAME, "tr")
    itemName = GetItemNameFromShopCartTable(driver, 0, rows_shop_table)
    rows_shop_table[0].find_elements(By.TAG_NAME, "td")[2].find_element(By.TAG_NAME, 'a').click()

    # check if the current page is the right page (title should contain the item name)
    assert itemName in driver.title


# ***********************************************************************************************************************************************

# Check if change the Quntity of the item the price will be bigger than the total price before change it
def test_ChangeQuantity(driver):
    driver.get('http://demostore.supersqa.com')

    # add 2 item in the cart and go to cart page
    Add2ItemToCart(driver)

    # get the total price of items before change the quntity
    rows_shop_table = driver.find_element(By.XPATH, '//*[@id="post-7"]/div/div/form/table/tbody').find_elements(
        By.TAG_NAME, "tr")
    PriceBeforeChangeQuantity = TotalPriceCalculate(driver, rows_shop_table)

    # change the quntity of some item (from 1 to 3)
    QuntityInput = rows_shop_table[0].find_element(By.TAG_NAME, "input")
    QuntityInput.clear()
    QuntityInput.send_keys('3')
    driver.find_element(By.NAME, 'update_cart').click()

    # waiting the quntity and the price is changed
    time.sleep(3)

    # get the total price of items after change the quntity
    rows_shop_table = driver.find_element(By.XPATH, '//*[@id="post-7"]/div/div/form/table/tbody').find_elements(
        By.TAG_NAME, "tr")
    PriceAfterChangeQuantity = TotalPriceCalculate(driver, rows_shop_table)

    # check if the total price after change the quntity will be bigger than the total price before change it
    assert PriceBeforeChangeQuantity < PriceAfterChangeQuantity
