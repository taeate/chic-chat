from time import time
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
class TimeChecker(MiddlewareMixin):
    def process_request(self,request:HttpRequest):
        start_time = time()
        request.COOKIES.update(start_time=start_time)
        print('timechecking')
        return self.get_response(request)
    
    def process_response(self,request:HttpRequest,response:HttpResponse):
        start_time = request.COOKIES.get('start_time')
        print(f"{time()-start_time:0.5f}sec")
        return response
