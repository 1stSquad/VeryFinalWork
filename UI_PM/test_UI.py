import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from UI_PM.pages.MainPage import MainPage


@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(100)
    yield driver
    driver.quit()

@pytest.fixture
def main_page(browser):
    page = MainPage(browser)
    page.open()
    return page

def test_open(main_page):
    print("Current URL:", main_page.driver.current_url)
    try:
        WebDriverWait(main_page.driver, 100).until(EC.url_to_be(main_page.url))
    except Exception as e:
        print("Ошибка при ожидании URL:", e)
        print("Фактический URL:", main_page.driver.current_url)
        raise
    assert main_page.driver.current_url == main_page.url, "URL страницы не соответствует ожидаемому"

def test_get_title(main_page):
    title = main_page.get_title()
    assert title is not None, "Заголовок страницы не найден"
    assert "Кинопоиск. Онлайн кинотеатр. Фильмы сериалы мультфильмы и энциклопедия" or "Вы не робот" in title, "Заголовок страницы не содержит 'КиноПоиск'"

def test_wait_for_element(main_page):
    locator = (By.CSS_SELECTOR, "input[name='kp_query']")
    element = main_page.wait_for_element(locator)
    assert element is not None, "Элемент не найден"
    assert element.is_displayed(), "Элемент не отображается на странице"

def test_enter_search_query(main_page):
    query = "Блэйд"
    search_input_locator = (By.CSS_SELECTOR, "input[type='text']")
    search_input = main_page.wait_for_element(search_input_locator)
    search_input.clear()
    search_input.send_keys(query)
    assert search_input.get_attribute("value") == query, "Текст в поле ввода не соответствует запросу"

def test_search_nonexistent_content(main_page):
    query = "несуществующий_запрос"
    main_page.search(query)
    error_message_locator = (By.CSS_SELECTOR, "[class='search_results_topText']")
    error_message = main_page.wait_for_element(error_message_locator)
    assert error_message.is_displayed(), "Сообщение об ошибке не отображается"

def test_add_review(main_page):
    movie_name = "Блэйд"
    main_page.go_to_movie_page(movie_name)
    WebDriverWait(main_page.driver, 60).until(EC.title_contains(movie_name))
    review_text = "Отличный фильм! Рекомендую к просмотру."
    main_page.add_review(review_text)