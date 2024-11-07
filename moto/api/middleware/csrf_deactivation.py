from django.utils.deprecation import MiddlewareMixin

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/'):  # Nur für API-Pfade
            setattr(request, '_dont_enforce_csrf_checks', True)