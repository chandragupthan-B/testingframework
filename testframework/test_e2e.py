import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from PageObject.homepage import Homepage
from PageObject.cartpage import CartPage
from utilities.Basesetup import basesetup


class TestGreenKart(basesetup):

    def test_e2e_product_order(self):

        log = self.getLogger()
        homepage = Homepage(self.driver)
        cartpage = CartPage(self.driver)

        prod_name = {}
        self.base_url()
        self.driver.implicitly_wait(5)

        homepage.search_bar().send_keys("ber")
        time.sleep(2)
        products = homepage.filtered_product() # render all filtered product
        log.info("Rendering all filtered product")
        for product in products:
            if product.find_element(By.XPATH, "h4").text not in prod_name:
                prod_name[product.find_element(By.XPATH, "h4").text] = [homepage.product_quantity(product),product.find_element(By.CLASS_NAME,"product-price")] # add the filtered product to list and verify wre

            homepage.add_to_cart_button(product).click() #click add to cart button

        log.info("the filtered product match the product in the list")
        homepage.cart_button()
        homepage.proceed_to_checkout()
        # check promo input box and confirmation message
        cartpage.promo_input_box().send_keys("rahulshettyacademy")
        cartpage.promo_confirm_button()
        basesetup.verify_the_element(self,(By.CLASS_NAME, 'promoInfo')) # expilicit wait and confirm the element appears
        assert cartpage.promo_info() == "Code applied ..!"


    def test_product_addtocart_and_quantity(self):
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        products = homepage.filtered_product()
        quantity_changer = homepage.quantity_changer(products[0])
        quantity_counter = 1
        log.info("adding 10 quantity for the product ")
        for i in range(10):
            quantity_changer.find_element(By.XPATH, "a[@class='increment']").click()
            quantity_counter += 1

        assert quantity_counter == int(homepage.product_quantity(products[0]).get_attribute("value")), log.critical('the product quantity does match with add value')
        log.info("The Incremented quantity matches the input quantity")
        log.info("minus 5 quantity for the product ")
        for i in range(5):
            quantity_changer.find_element(By.XPATH, "a[@class='decrement']").click()
            quantity_counter -= 1

        assert quantity_counter == int(quantity_changer.find_element(By.XPATH, 'input[@class="quantity"]').get_attribute("value"))
        log.info("The decremented  quantity matches the quantity of the product")

        log.info("Try to reduce the quantity below minimum quantity")
        homepage.product_quantity(products[0]).clear()
        homepage.product_quantity(products[0]).send_keys('1')
        quantity_changer.find_element(By.XPATH, "a[@class='decrement']").click()

        assert int(homepage.product_quantity(products[0]).get_attribute("value")) == 1
        log.info("The minimum quatity for product is not below zero")

    def test_add_to_cart_button_in_product(self):
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        products = homepage.filtered_product()
        homepage.add_to_cart_button(products[0]).click()

        assert "✔ ADDED" == homepage.add_to_cart_button(products[0]).text, log.error('the add to cart button is not '
                                                                                     'changed to "Added" when clicked')
        log.info("ADDED text appeared after add to cart button is clicked")

    def test_empty_cart_dropdown(self):
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        cart_dropdown = homepage.cart_preview_dropdown()
        if cart_dropdown.find_element(By.CSS_SELECTOR,".empty-cart"):
            assert cart_dropdown.find_element(By.CSS_SELECTOR, ".empty-cart h2").text == ""

    def test_disabled_proceed_to_checkout_button(self):
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        checkout_button = self.driver.find_element(By.XPATH,"//button[text() = 'PROCEED TO CHECKOUT']").is_enabled()
        assert checkout_button == True


    def test_cart_dropbox(self):

        prod_name = {}
        cart_product = {}
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        products = homepage.filtered_product()
        log.info("adding the products to the cart")
        for i in range(0,4):
            quantity = homepage.product_quantity(products[i]).get_attribute("value")
            price = products[i].find_element(By.CLASS_NAME,"product-price").text
            prod_name[products[i].find_element(By.XPATH, "h4").text] = [quantity, price, int(quantity)*int(price)]
                # add the filtered product to list and verify
            homepage.add_to_cart_button(products[i]).click()  # click add to cart button
        homepage.cart_button()
        product_in_cart_dropdown = homepage.cart_dropdown_item()
        for product in product_in_cart_dropdown:
            quantity = ''.join(q for q in product.find_element(By.CSS_SELECTOR,".quantity").text if q.isdigit())
            price = product.find_element(By.CSS_SELECTOR, ".product-price").text
            total_price = product.find_element(By.CSS_SELECTOR,".amount").text
            cart_product[
                product.find_element(By.CSS_SELECTOR,".product-name").text] = [ quantity,price,int(total_price)]
        log.info("verifing the product in the cart dropdown element and it's values")
        assert prod_name == cart_product , log.critical("the added product is not appeared in the cart dropdown or the values are mismatched")

    def test_cart_dropdown_x_button(self):
        prod_name = []
        remove_prod = []
        self.base_url()
        log = self.getLogger()
        homepage = Homepage(self.driver)
        products = homepage.filtered_product()
        log.info("adding the products to the cart")
        for i in range(0, 4):
            homepage.add_to_cart_button(products[i]).click()  # click add to cart button
            prod_name.append(products[i].find_element(By.XPATH, "h4").text)
        homepage.cart_button()
        product_in_cart_dropdown = homepage.cart_dropdown_item()
        for i in range(0,len(product_in_cart_dropdown),2):
            remove_prod.append(product_in_cart_dropdown[i].find_element(By.CSS_SELECTOR,".product-name").text)
            product_in_cart_dropdown[i].find_element(By.CSS_SELECTOR,".product-remove").click()

        assert prod_name != remove_prod

    def test_flight_booking(self):
        homepage = Homepage(self.driver)
        log = self.getLogger()
        homepage.flight_booking_link()
        windowopen = self.driver.window_handles
        self.driver.switch_to.window(windowopen[1])
        assert self.driver.current_url == 'https://rahulshettyacademy.com/dropdownsPractise/'
        self.driver.close()
        self.driver.switch_to.window(windowopen[0])

    def test_cart_product_list(self):
        prod_name={}
        self.base_url()
        homepage = Homepage(self.driver)
        cartpage = CartPage(self.driver)
        log = self.getLogger()
        products = homepage.filtered_product()
        log.info("adding the products to the cart")
        for i in range(0, 4):
            quantity = homepage.product_quantity(products[i]).get_attribute("value")
            price = products[i].find_element(By.CLASS_NAME, "product-price").text
            prod_name[products[i].find_element(By.XPATH, "h4").text] = [quantity, price, int(quantity) * int(price)]
            # add the filtered product to list and verify
            homepage.add_to_cart_button(products[i]).click()  # click add to cart button
        homepage.cart_button()
        homepage.proceed_to_checkout()
        products_table = cartpage.products_list_table()
        products = products_table.find_elements(By.XPATH,'tr')
        for p in products:
            print(len(p.find_elements(By.XPATH,'td')))

























