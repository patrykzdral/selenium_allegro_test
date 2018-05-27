from selenium import webdriver
import time
from selenium_results.order import Order
from selenium_results.researcher_result import \
    OrdersHistory
import pickle
import collections
# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.maximize_window()

# navigate to the application home page
driver.get('https://allegro.pl/myaccount/')

login_box = driver.find_element_by_name('username')
login_box.send_keys('xxx')

passwd_box = driver.find_element_by_name('password')
passwd_box.send_keys('xxx')

login_box.submit()
# daj czas na wypadek captcha
# 10 sekund
time.sleep(10)
inputElement=driver.find_element_by_xpath(".//input[@placeholder='czego szukasz?']").send_keys("lenovo y-50-70")
time.sleep(2)
inputElement=driver.find_element_by_xpath(".//input[@class='metrum-search__submit _xepa8 _1c5ga _1amu3']").click()

# Rozwinięcie listy z opcjami sortowania zamówień.
# Wybór sortowania - od nijniższej ceny.

driver.find_element_by_xpath(".//button[@class='sort__sorting-list__btn__8xObu']").click()
time.sleep(2)
driver.find_element_by_xpath("//a[contains(text(), 'od najniższej')]").click()
#driver.find_element_by_xpath(".//select[@class='_1akfs _o2u5x _1pffh']").click()
#driver.find_element_by_xpath("//*[contains(text(), 'cena z dostawą: od najniższej')]").click()

driver.find_element_by_xpath("//*[contains(text(), 'Lenovo Y50-70 i7-4510U 2x3,1GHz 8GB 1TB Win10')]").click()
time.sleep(4)
driver.find_element_by_xpath("//*[contains(text(), 'dodaj do koszyka')]").click()
time.sleep(2)

#cofnięcie do poprzedniej strony
driver.back()
driver.back()
time.sleep(2)

driver.find_element_by_xpath("//*[contains(text(), 'Lenovo Y50-70 /GTX 960/ 8 GB RAM/Core i5/ 15,6')]").click()
time.sleep(2)
driver.find_element_by_xpath("//*[contains(text(), 'dodaj do koszyka')]").click()
time.sleep(2)
driver.find_element_by_xpath("//*[contains(text(), 'kontynuuj zakupy')]").click()
time.sleep(2)

#cofnięcie do poprzedniej strony
driver.back()
time.sleep(2)


driver.find_element_by_xpath("//*[contains(text(), 'USB board Lenovo Y50-70 LS-B113P ZIVY2/ZIVY3')]").click()
time.sleep(2)
driver.find_element_by_xpath("//*[contains(text(), 'dodaj do koszyka')]").click()
time.sleep(2)
driver.find_element_by_xpath("//*[contains(text(), 'przejdź do koszyka')]").click()
time.sleep(2)


# Rozwinięcie listy z opcją wejścia w historię kupionych
driver.find_element_by_xpath(".//button[@class='_iu5pr _z41ha fee54_3GU3E "
                             "fee54_3U14k']") \
    .click()
time.sleep(2)
# wejście do historii
driver.find_element_by_xpath(
    "//a[contains(text(),'kupione')]").click()



# Pobranie zawartości kontenera przechowującego zamówienia.
orders_sections = driver \
    .find_element_by_xpath(".//div[@class='listing ng-scope']") \
    .find_elements_by_xpath(".//section[@class='panel panel-default "
                            "panel-order ng-scope']")

# Wyłuskanie pożądanych elementów charakterystycznych zamówień.
researcherResult = OrdersHistory()
for order_section in orders_sections:
    number_of_elements_in_order = int(order_section.find_element_by_xpath(
        ".//offer-quantity[@class='didascalia-color ng-isolate-scope']")
                                      .text.split(" ", 1)[0])

    researcherResult.orders = Order(
        seller=str(order_section.find_element_by_xpath(
            ".//a[@class='seller-login ng-scope']").text),
        purchase_date=order_section.find_element_by_xpath(
            ".//div[@class='order-status-date ng-binding']").text[13:],
        price=float(order_section.find_element_by_xpath(
            ".//formatted-price[@amount='ctrl.offerPriceAmount']").text[
                    :-3].replace(',', '.')),
        price_with_delivery=float(order_section.find_element_by_xpath(
            ".//formatted-price[@amount='order.totalCost.amount']").text[
                                  :-3].replace(',', '.')),
        number_of_elements=number_of_elements_in_order)

print("Wynik poszukiwań:")
for order in researcherResult.orders:
    print(order)
print("\nIlość zamówień:")
print(len(researcherResult.orders))

# Rozwinięcie listy z m.in. opcją wylogowania.
driver.find_element_by_xpath(".//button[@class='_iu5pr _z41ha fee54_3GU3E "
                             "fee54_3U14k']") \
    .click()
time.sleep(2)

try:
    with open('previous_test.pkl', 'rb') as previous_test_result_input:
        previousResearcherResult = pickle.load(previous_test_result_input)
        if researcherResult == previousResearcherResult:
            print("\nWynik pozytywny")
        else:
            print("\nWynik negatywny")
            print("\nWynik poszukiwań z poprzedniego testu:")
            for order in researcherResult.orders:
                print(order)
            print("\nIlość zamówień z poprzedniego testu:")
            print(len(previousResearcherResult.orders))
except FileNotFoundError:
    with open('previous_test.pkl', 'wb') as output:
        pickle.dump(researcherResult, output, pickle.HIGHEST_PROTOCOL)
        print("\nWynik testu regresyjnego: brak (plik z wynikiem poprzedniego"
"testu nie istnieje).share")

# Wylogowanie z serwisu Allegro.
driver.find_element_by_xpath(
    "//a[contains(text(),'wyloguj')]").click()
# close the browser window
driver.quit()
