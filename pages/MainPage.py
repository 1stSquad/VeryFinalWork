from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = 'https://www.kinopoisk.ru/'
        self.search_input_locator = (By.CSS_SELECTOR, "input[name='kp_query']")

    def open(self):
        try:
            self.driver.get(self.url)
        except Exception as e:
            print(f"Ошибка при открытии страницы: {e}")

    def get_title(self):
        try:
            return self.driver.title
        except Exception as e:
            print(f"Ошибка при открытии страницы: {e}")

    def wait_for_element(self, locator, timeout=100):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            print(f"Элемент не найден: {e}")
            raise

    def enter_search_query(self, query):
        try:
            search_input = self.wait_for_element(self.search_input_locator)
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Ошибка при вводе запроса: {e}")

    def search(self, query):
        try:
            self.enter_search_query(query)
        except Exception as e:
            print(f"Ошибка при выполнении поиска: {e}")

    def go_to_movie_page(self, movie_name):
        self.search(movie_name)
        movie_link_locator = (By.CSS_SELECTOR, "div[class='element most_wanted'] div[class='info'] a[class='js-serp-metrika']")
        movie_link = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located(movie_link_locator))
        movie_link.click()

    def wait_and_click(self, locator, timeout=60):
        """Вспомогательный метод для ожидания и клика по элементу."""
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def wait_and_send_keys(self, locator, text, timeout=60):
        """Вспомогательный метод для ожидания и ввода текста."""
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        element.send_keys(text)

    def add_review(self, review_text):
        # Локаторы
        ADD_REVIEW_BUTTON = (By.XPATH, "//button[contains(text(),'Написать рецензию')]")
        REVIEW_TYPE_BUTTON = (By.XPATH, "//div[@class='styles_selectButton__7pOFy styles_button__3dBmr styles_bold__BehKN']")
        POSITIVE_REVIEW_BUTTON = (By.XPATH, "//div[@id='user-reviews']//label[1]")
        REVIEW_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Текст']")
        CAPTCHA_CHECKBOX = (By.XPATH, "//input[@id='js-button']")
        SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Опубликовать рецензию')]")

        # Шаг 1: Нажать кнопку "Написать рецензию"
        self.wait_and_click(ADD_REVIEW_BUTTON)
        # Шаг 2: Выбрать тип рецензии
        self.wait_and_click(REVIEW_TYPE_BUTTON)
        # Шаг 3: Выбрать позитивную рецензию
        self.wait_and_click(POSITIVE_REVIEW_BUTTON)
        # Шаг 4: Ввести текст рецензии
        self.wait_and_send_keys(REVIEW_TEXTAREA, review_text)
        # Шаг 5: Пройти капчу (если требуется)
        self.wait_and_click(CAPTCHA_CHECKBOX)
        # Шаг 6: Опубликовать рецензию
        self.wait_and_click(SUBMIT_BUTTON)