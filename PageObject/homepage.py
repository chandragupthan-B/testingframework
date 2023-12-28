from selenium.webdriver.common.by import By

from utilities.Basesetup import basesetup

class Homepage:

    search_key = (By.CSS_SELECTOR, ".search-keyword")
    filter_products = (By.XPATH, '//div[@class="products"]/div')
    quantity_element = (By.XPATH,"div[@class='stepper-input']")
    quantity = (By.XPATH, 'input[@class="quantity"]')
    add_to_cart = (By.XPATH, 'div/button')
    cart_details = (By.XPATH, '//div[@class = "cart-info"]/table/tbody/tr/td/strong')
    cart_icon = (By.XPATH, '//a[@class="cart-icon"]/img')
    checkout_button = (By.XPATH, "//button[text()='PROCEED TO CHECKOUT']")
    cart_dropdown = (By.CSS_SELECTOR, ".cart-preview")
    cart_items = (By.CSS_SELECTOR,".cart-item")
    flight_booking = (By.LINK_TEXT,"Flight Booking")


    def __init__(self,driver):
        self.driver = driver

    def search_bar(self):
        return self.driver.find_element(*Homepage.search_key)

    def filtered_product(self):
        return self.driver.find_elements(*Homepage.filter_products)

    def quantity_changer(self,product):
        return product.find_element(*Homepage.quantity_element)

    def product_quantity(self,product):
        quantity_element = self.quantity_changer(product)
        return quantity_element.find_element(*Homepage.quantity)

    def add_to_cart_button(self,product):
        return product.find_element(*Homepage.add_to_cart)

    def cart_info_detials(self):
        return self.driver.find_elements(*Homepage.cart_details)

    def cart_button(self):
        self.driver.find_element(*Homepage.cart_icon).click()

    def proceed_to_checkout(self):
        self.driver.find_element(*Homepage.checkout_button).click()

    def cart_preview_dropdown(self):
        return self.driver.find_element(*Homepage.cart_dropdown)

    def cart_dropdown_item(self):
        items = self.cart_preview_dropdown()
        return items.find_elements(*Homepage.cart_items)

    def flight_booking_link(self):
        return self.driver.find_element(*Homepage.flight_booking).click()

