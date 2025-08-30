import time
import logging

logger = logging.getLogger(__name__)

class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        
        # Process the request and get the response
        response = self.get_response(request)
        
        duration = time.time() - start_time
        logger.info(f"{request.path} took {duration:.4f} seconds")
        
        return response
