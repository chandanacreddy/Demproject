from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Locators import Locators
import time

#driver = webdriver.Chrome('..\\Drivers\\chromedriver.exe')
#----Code to launch the website---#
def verify_website_launch():
    try:
        global driver
        driver = webdriver.Chrome('..\\Drivers\\chromedriver.exe')
        driver.implicitly_wait(2)
        driver.maximize_window()
        driver.get(Locators.URL)
        Website_Title = driver.title
        if Website_Title == Locators.SWAGLAB_PAGE:
            print("Website launched successfully")
            return True
        else:
            print("website not launched")
            driver.close()
            return False
    except:
        print("Exception in verify_website_launch function ")
        driver.close()
        return False

#----Login to the account---#
def Account_Login_Check(username,password):
    try:
        verify_website_launch()
        driver.find_element_by_id(Locators.USER_TEXTBOX_NAME_ID).send_keys(username)
        driver.find_element_by_id(Locators.PASSWORD_TEXTBOX_NAME_ID).send_keys(password)
        driver.find_element_by_id(Locators.LOGIN_ID).click()
    except:
        print("Exception in Account_Login_Check function ")
        driver.close()
        return False

#------Successfully log in to  the website validation--#
def Validate_User_Entered_into_page():
    try:
        Account_Login_Check(Locators.USER_NAME, Locators.PASSWORD)
        time.sleep(1)
        Peekimage = driver.find_element_by_xpath(Locators.PEEK_IMAGE_XPATH).is_displayed()
        if Peekimage == True:
            print("Successfully Logged in")
        else:
            print("Error in Log_in")
            driver.close()
            return False
    except:
        print("Exception in Validate_User_Entered_into_page function ")
        driver.close()
        return False

#---------Scenario 1------------#
def test_Verify_product_added_to_cart():
    try:
        Validate_User_Entered_into_page()
        Added_Product_item = driver.find_element_by_class_name(Locators.PRODUCT_CLASSNAME).text
        print("Selected product to add to cart is:" +Added_Product_item)
        driver.find_element_by_id(Locators.ADD_TO_CART_ID).click()
        Remove_cart_option = driver.find_element_by_id(Locators.REMOVE_FROM_CART_ID).is_displayed()
        time.sleep(2)
        if Remove_cart_option == True:
            print("Product is added to the cart successfully")
        else:
            print("Product is not added to the cart")
            driver.close()
            return False
        driver.find_element_by_class_name(Locators.SHIPPING_CART_BUTTON_CLASSNAME).click()
        if driver.find_element_by_id(Locators.CHECK_OUT_ID).is_displayed():
            driver.find_element_by_id(Locators.CHECK_OUT_ID).click()
            if driver.find_element_by_id(Locators.CONTINUE_ID).is_displayed():
                driver.find_element_by_id(Locators.FIRSTNAME_ID).send_keys(Locators.FIRSTNAME)
                driver.find_element_by_id(Locators.LASTNAME_ID).send_keys(Locators.LASTNAME)
                driver.find_element_by_id(Locators.ZIPCODE_ID).send_keys(Locators.ZIPCODE)
                driver.find_element_by_id(Locators.CONTINUE_ID).click()
                if driver.find_element_by_class_name(Locators.PRODUCT_CLASSNAME).is_displayed():
                    Checkout_product_item= driver.find_element_by_class_name(Locators.PRODUCT_CLASSNAME).text
                    if driver.find_element_by_id(Locators.FINISH_ID).is_displayed():
                        if Added_Product_item==Checkout_product_item:
                            print("The checkout out product is same as the selected product added to the cart is:"+Checkout_product_item)
                            driver.find_element_by_id(Locators.FINISH_ID).click()
                            time.sleep(1)
                            if driver.find_element_by_xpath(Locators.CHECK_OUT_COMPLETED_XPATH).is_displayed():
                                Checkout_successfull = driver.find_element_by_xpath(Locators.CHECK_OUT_COMPLETED_XPATH).text
                                if Checkout_successfull == Locators.CHECK_OUT_MESSAGE:
                                    print("Correct product is Ordered")
                                    driver.close()
                                    return True
                                else:
                                    print("product is not ordered correctly")
                                    driver.close()
                                    return False
                        else:
                            print("The checkout out product is not same as the selected product added to the cart is:"+Checkout_product_item)
                            return False
                    else:
                        print("Not Entered to delivery information page")
                        return False
                else:
                    print("Product is not selected one to checkout")
                    return False
            else:
                print("Not Entered to checkout page")
                return False
    except:
        print("Exeception in test_Verify_product_added_to_cart function")
        driver.close()
        return False

###Scenario 2
def test_Verify_Particular_Product():
    try:
        product_items = ""
        Validate_User_Entered_into_page()
        item_list = driver.find_elements_by_class_name(Locators.PRODUCT_CLASSNAME)
        for items in item_list:
            items = items.text
            product_items = product_items+items+","
        print("List of product names found on page is:"+product_items)
        if Locators.PARTICULAR_PRODUCT in product_items:
            print("The particular product is available in the given list is : " + Locators.PARTICULAR_PRODUCT)
            driver.close()
            return True
        else:
            print("The particular product is not available in the given list is : " + Locators.PARTICULAR_PRODUCT)
            driver.close()
            return False
    except:
        print("Exception in test_Verify_Particular_Product function")
        driver.close()
        return False


###Scenario 3
def test_Verify_price_with_particular_product():
    try:
        productprice = ""
        Validate_User_Entered_into_page()
        price_list = driver.find_elements_by_class_name(Locators.PRICE_CLASSNAME)
        for price in price_list:
            prices=price.text
            productprice = productprice + prices + ","
        print("List of prices for all products is:"+productprice)
        Dollarremoval = productprice.replace("$","")
        print("List of prices for all products after removing $ symbol:"+Dollarremoval)
        driver.find_element_by_class_name(Locators.PRODUCT_CLASSNAME).click()
        Backtoproduct=driver.find_element_by_id(Locators.BACK_TO_PRODUCT).is_displayed()
        if Backtoproduct==True:
            print("user lands to the product listing page ,on click of particular product")
        else:
            print("user didn't land to the product listing page ,on click of particular product")
            return False
        Individual_price = driver.find_element_by_class_name(Locators.PRICE_RANGE_CLASSNAME).text
        Amount = Individual_price.replace("$","")
        if Amount in Dollarremoval:
            print("Price is validated with the selected product individual page is: "+Amount)
            driver.close()
            return True
        else:
            print("Price is not matching for the selected product individual page")
            driver.close()
            return False
    except:
        print("Exception in test_Verify_price_with_particular_product function")
        driver.close()
        return False


###scenario_4
def test_Invalid_credential_validation():
    try:
        Account_Login_Check(Locators.INVALID_USERNAME,Locators.INVALID_PASSWORD)
        ErrorMessage = driver.find_element_by_xpath(Locators.ERROR_MSG_XPATH).text
        time.sleep(1)
        if ErrorMessage == Locators.ERROR_TEXT_MSG:
            print("Invalid username and pwd error message is : "+ErrorMessage)
            driver.close()
            return True
        else:
            print("Invalid username and pwd error message not displayed")
            driver.close()
            return False
    except:
        driver.close()
        print("Exception in Invalid_credential_validation function ")
        return False

test_Verify_product_added_to_cart()
test_Verify_Particular_Product()
test_Verify_price_with_particular_product()
test_Invalid_credential_validation()
