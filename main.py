from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import time

url = "https://www.audible.com/search?keywords=book&node=18573211011"

browser_options = webdriver.ChromeOptions()
browser_options.add_experimental_option("detach", True)

heading = ["title", "author", "subtitle", "language", "length", "release_date", "rating_stars", "reviews"]
driver = webdriver.Chrome(options=browser_options)
# driver.maximize_window()


def load_books_one_page():
    def provide_element_text(web_section, css_selector):
        try:
            element = web_section.find_element(By.CSS_SELECTOR, css_selector)
            return element.text.replace(",", "|")
        except NoSuchElementException:
            return "None"

    books = driver.find_elements(By.CLASS_NAME, 'productListItem')
    loaded_records = []

    for book in books:
        title = provide_element_text(book, 'h3 a')
        author = provide_element_text(book, '.authorLabel a')
        subtitle = provide_element_text(book, '.subtitle')
        language = provide_element_text(book, '.languageLabel')
        length = provide_element_text(book, '.runtimeLabel')
        release_date = provide_element_text(book, '.releaseDateLabel')
        rating_stars = provide_element_text(book, 'li.bc-list-item.ratingsLabel > span.bc-text.bc-pub-offscreen')
        reviews = provide_element_text(book,
                                       'li.bc-list-item.ratingsLabel > span.bc-text.bc-size-small.bc-color-secondary')

        record = [title, author, subtitle, language, length, release_date, rating_stars,
                  reviews]

        loaded_records.append(record)
    return loaded_records


def save_records_from_one_page(records_list, loop_num):
    try:
        file = open('data.csv', mode="r")
        file.close()
    except FileNotFoundError:
        file = open('data.csv', mode="w")
        file.close()
    finally:
        with open('data.csv', newline='', encoding='utf-8', mode="a") as file:
            writer = csv.writer(file)
            if loop_num == 0:
                writer.writerow(heading)
            for record in records_list:
                writer.writerow(record)


def change_page():
    next_page = driver.find_element(By.CSS_SELECTOR, '.nextButton a')
    next_page.click()


driver.get(url)
for loop in range(15):
    records = load_books_one_page()
    change_page()
    time.sleep(2)
    save_records_from_one_page(records, loop)

driver.quit()
