from django.http import JsonResponse
from django.http import Http404
from config.custom_exceptions import BaseCustomException

class ExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        error_info = self._get_error_info(exception)

        response_data = self._create_unified_response(request, error_info)

        return JsonResponse(
            response_data,
            status=error_info['status_code'] if 'status_code' in error_info else 500,
        )
    
    def _get_error_info(self, exception):
        if isinstance(exception, BaseCustomException):
            return {
                'code': exception.code,
                'message': exception.detail,
                'status_code': exception.status_code
            }

        return {
            'code': 'INTERNAL-SERVER-ERROR',
            'message': 'An internal server error occurred.',
            'status_code': 500
        }
        
    def _create_unified_response(self, request, error_info):
        return {
            'success': False,
            'error': {
                'code': error_info.get('code', 'UNKNOWN-ERROR'),
                'message': error_info.get('message', 'An error occurred.'),
                'status_code': error_info.get('status_code', 500)
            }
        }
