from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class MyException(MiddlewareMixin):

    def process_request(self, request):
        print('自定义的process_request')
        return None

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('自定义process_view')
        return None

    def process_template_response(self, request, response):
        print('自定义process_template_response')
        return response

    def process_response(self, request, response):
        print('自定义process_response')
        return response

    def process_exception(self, request, exception):
        print('自定义process_exception')
        return HttpResponse(exception)