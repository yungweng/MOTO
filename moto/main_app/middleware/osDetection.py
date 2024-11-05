from django.http import HttpResponseRedirect
from django.urls import reverse
from main_app.models import Raum_Belegung
from main_app.urls import (
    allowed_urls_web, allowed_urls_android, 
    main_url_android, main_url_web, 
    allowed_urls_android_no_room, 
    main_url_android_no_room, urls_apis
)
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
        
        # Überprüfung, ob die Anfrage von einem Browser kommt
        if self.is_browser(user_agent):
            # Logik für Browser
            if not (path in allowed_urls_web or name_path in allowed_urls_web):
                return HttpResponseRedirect(reverse(main_url_web))

        # Anfrage verarbeiten
        response = self.get_response(request)
        return response

    def is_browser(self, user_agent):
        """Überprüft, ob der User-Agent auf einen Browser hinweist."""
        browsers = ['Chrome', 'Firefox', 'Safari', 'Opera', 'Edge']
        return any(browser in user_agent for browser in browsers)
