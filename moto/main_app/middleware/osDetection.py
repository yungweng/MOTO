from django.http import HttpResponseRedirect
from django.urls import reverse
from main_app.models import Raum_Belegung
from main_app.urls import allowed_urls_web, allowed_urls_android, main_url_android, main_url_web, allowed_urls_android_no_room, main_url_android_no_room
from django.urls import resolve

class OsDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        path = request.path
        name_path = ''
        try:
            match = resolve(path)
            name_path = match.url_name
        except:
            pass
        if not 'Android' in user_agent:    #IOS for debugging and testing    
            if not (path in allowed_urls_web or name_path in allowed_urls_web):
                return HttpResponseRedirect(reverse(main_url_web)) 
        elif 'Android' in user_agent:        #IOS for debugging and testing
            if(path in allowed_urls_android or name_path in allowed_urls_android):
                if 'device_id' in request.COOKIES:
                    device_id = request.COOKIES.get('device_id')                
                    if not(Raum_Belegung.objects.filter(tablet_id=device_id).exists()):
                        if not(path in allowed_urls_android_no_room or name_path in allowed_urls_android_no_room):
                            return HttpResponseRedirect(reverse(main_url_android_no_room))
            else:
                return HttpResponseRedirect(reverse(main_url_android))    
        response = self.get_response(request)

        return response