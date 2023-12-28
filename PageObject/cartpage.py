from selenium.webdriver.common.by import By


class CartPage:

    promo_box = (By.CSS_SELECTOR, ".promoCode")
    promo_button = (By.CLASS_NAME, 'promoBtn')
    promo_text = (By.CLASS_NAME, 'promoInfo')
    products_list = (By.XPATH,'//table[@class="cartTable"]/tbody')

    def __init__(self,driver):
        self.driver = driver

    def promo_input_box(self):
        return self.driver.find_element(*CartPage.promo_box)

    def promo_confirm_button(self):
        self.driver.find_element(*CartPage.promo_button).click()

    def promo_info(self):
        return self.driver.find_element(*CartPage.promo_text).text

    def products_list_table(self):
        return self.driver.find_element(*CartPage.products_list)
