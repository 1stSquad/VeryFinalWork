import pytest
import allure
from API_PM.MovieAPI import MovieAPI
from config import BASE_URL, API_KEY

@pytest.fixture
def movie_api():
    return MovieAPI(BASE_URL, API_KEY)

@allure.feature("Поиск фильмов")
@allure.story("Поиск фильма по названию")
@pytest.mark.parametrize("movie_title, expected_movie_id", [("Один дома 3", 20789)])
def test_search_movie_by_title(movie_title, expected_movie_id, movie_api):
    with allure.step(f"Поиск фильма по названию: {movie_title}"):
        response = movie_api.search_movie_by_title(movie_title)
        data = response.json()
        assert data.get("docs"), "Нет результатов поиска"
        first_movie = data["docs"][0]
        assert first_movie["id"] == expected_movie_id, f"Ожидался фильм с ID {expected_movie_id}, но получен {first_movie['id']}"

@allure.feature("Получение информации о фильме")
@allure.story("Получение фильма по ID")
@pytest.mark.parametrize("movie_id, expected_movie_title", [(20789, "Один дома 3")])
def test_get_movie_by_id(movie_id, expected_movie_title, movie_api):
    with allure.step(f"Получение фильма по ID: {movie_id}"):
        response = movie_api.get_movie_by_id(movie_id)
        data = response.json()
        assert data, "Нет данных о фильме"
        assert data.get("name") == expected_movie_title, f"Ожидался фильм с названием '{expected_movie_title}', но получен '{data.get('name')}'"
        assert data.get("id") == movie_id, f"Ожидался фильм с ID {movie_id}, но получен {data.get('id')}"

@allure.feature("Получение случайного фильма")
@allure.story("Получение случайного фильма с параметрами")
@pytest.mark.parametrize("params", [{"genres": "триллер", "countries": "Германия", "ageRating": "18", "limit": 1}])
def test_get_random_movie(params, movie_api):
    with allure.step("Получение случайного фильма с параметрами"):
        response = movie_api.get_random_movie(params["genres"], params["countries"], params["ageRating"], params["limit"])
        assert response.status_code == 200, f"Ожидался статус код 200, но получен {response.status_code}"
        movie_data = response.json()
        assert isinstance(movie_data, dict), "Ответ не является словарем"
        allure.attach("Информация о фильме", f"""
            Название: {movie_data.get('name', 'Название отсутствует')}
            ID: {movie_data.get('id', 'ID отсутствует')}
            Возрастной рейтинг: {movie_data.get('ageRating', 'Рейтинг отсутствует')}
            Жанры: {', '.join([genre.get('name', 'Жанр отсутствует') for genre in movie_data.get("genres", [])])}
            Страны: {', '.join([country.get('name', 'Страна отсутствует') for country in movie_data.get("countries", [])])}
        """)
        assert "id" in movie_data, "Ответ не содержит ключа 'id'"
        assert "name" in movie_data, "Ответ не содержит ключа 'name'"
        assert "genres" in movie_data, "Ответ не содержит ключа 'genres'"
        assert "countries" in movie_data, "Ответ не содержит ключа 'countries'"
        assert movie_data["ageRating"] == int(params["ageRating"]), f"Возрастной рейтинг не соответствует ожидаемому: {movie_data['ageRating']}"
        assert any(genre["name"] == params["genres"] for genre in movie_data["genres"]), f"Жанр '{params['genres']}' не найден"
        assert any(country["name"] == params["countries"] for country in movie_data["countries"]), f"Страна '{params['countries']}' не найдена"

@allure.feature("Поиск фильмов")
@allure.story("Поиск фильма с пустым названием")
def test_search_movie_with_empty_title(movie_api):
    with allure.step("Поиск фильма с пустым названием"):
        response = movie_api.search_movie_by_title("")
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"
        data = response.json()
        assert data.get("docs"), "Нет результатов поиска"

@allure.feature("Поиск фильмов")
@allure.story("Поиск фильма по частичному названию")
@pytest.mark.parametrize("partial_title, expected_movie_id", [("Бин", 161087)])
def test_search_movie_by_partial_title(partial_title, expected_movie_id, movie_api):
    with allure.step(f"Поиск фильма по частичному названию: {partial_title}"):
        response = movie_api.search_movie_by_title(partial_title)
        data = response.json()
        assert response.status_code == 200, f"Ожидался статус-код 200, но получен {response.status_code}"
        assert data.get("docs"), "Нет результатов поиска"
        assert any(movie["id"] == expected_movie_id for movie in data["docs"]), f"Фильм с ID {expected_movie_id} не найден"

@allure.feature("Получение информации о фильме")
@allure.story("Получение фильма по неверному ID")
@pytest.mark.parametrize("invalid_movie_id", ["не число"])
def test_get_movie_by_invalid_id(invalid_movie_id, movie_api):
    with allure.step(f"Получение фильма по неверному ID: {invalid_movie_id}"):
        response = movie_api.get_movie_by_id(invalid_movie_id)
        assert response.status_code == 400, f"Ожидался статус-код 400, но получен {response.status_code}"

@allure.feature("Получение информации о фильме")
@allure.story("Получение фильма по несуществующему ID")
@pytest.mark.parametrize("movie_id", [123456789])
def test_get_movie_by_non_existent_id(movie_id, movie_api):
    with allure.step(f"Получение фильма по несуществующему ID: {movie_id}"):
        response = movie_api.get_movie_by_id(movie_id)
        assert response.status_code == 400, f"Ожидался статус-код 400, но получен {response.status_code}"