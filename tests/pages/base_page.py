class BasePage:
    def __init__(self, browser, rand_number_for_entites):
        self.browser = browser
        self.rand_number_for_entities = rand_number_for_entites

    def find(self, args):
        return self.browser.find_element(*args)

    
    
    
