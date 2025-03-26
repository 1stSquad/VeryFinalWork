from BaseAPI import BaseAPI


class MovieAPI(BaseAPI):
    def search_movie_by_title(self, title, limit=5):
        params = {
            "page": 1,
            "limit": limit,
            "query": title
        }
        return self.get("movie/search", params=params)

    def get_movie_by_id(self, movie_id):
        return self.get(f"movie/{movie_id}")

    def get_random_movie(self, genres, countries, age_rating, limit=1):
        params = {
            "genres.name": genres,
            "countries.name": countries,
            "ageRating": age_rating,
            "limit": limit
        }
        return self.get("movie/random", params=params)

