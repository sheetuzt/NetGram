from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DATABASE_NAME

class Database:
    _client = None
    _db = None

    def __init__(self):
        if Database._client is None:
            Database._client = AsyncIOMotorClient(MONGO_URI)
            Database._db = Database._client[DATABASE_NAME]

        self.client = Database._client
        self.db = Database._db
        self.movies = self.db.movies

    async def get_movies(self, skip=0, limit=20):
        cursor = self.movies.find({}).skip(skip).limit(limit).sort("date_added", -1)
        return await cursor.to_list(length=limit)

    async def get_movie_by_id(self, movie_id):
        return await self.movies.find_one({"message_id": int(movie_id)})

    async def search_movies(self, query, skip=0, limit=20):
        cursor = self.movies.find(
            {"title": {"$regex": query, "$options": "i"}}
        ).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def filter_movies(self, genre=None, language=None, quality=None, skip=0, limit=20):
        filter_query = {}
        if genre:
            filter_query["genres"] = {"$in": [genre]}
        if language:
            filter_query["language"] = {"$regex": language, "$options": "i"}
        if quality:
            filter_query["quality"] = {"$regex": quality, "$options": "i"}

        cursor = self.movies.find(filter_query).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_popular_movies(self, skip=0, limit=20):
        cursor = self.movies.find({"imdbRating": {"$exists": True}})\
            .sort("imdbRating", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)

    async def get_recent_movies(self, skip=0, limit=20):
        cursor = self.movies.find({})\
            .sort("date_added", -1).skip(skip).limit(limit)
        return await cursor.to_list(length=limit)


db = Database()
