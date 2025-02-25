from scrapy.http import HtmlResponse, TextResponse
from scrapy.utils.python import to_bytes
from databaseCache import DatabaseCache

class CacheMiddleware:
    def __init__(self):
        self.cache = DatabaseCache()

    def process_request(self, request, spider):
        cached_response = self.cache.get_cached_response(request.url)

        if cached_response:
            if isinstance(cached_response, str):
                cached_response = cached_response.encode('utf-8')

                return HtmlResponse(url=request.url, body=cached_response, encoding='utf-8')
        
        return None

    def process_response(self, request, response, spider):
        if response.status == 200:
            self.cache.store_response(request.url, to_bytes(response.body))
        return response