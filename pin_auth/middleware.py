from django.utils import timezone

class ShoulderSurfingProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_id' in request.session:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                idle_seconds = (timezone.now() - last_activity).total_seconds()
                if idle_seconds > 300:  
                    if 'user_id' in request.session:
                        del request.session['user_id']

            request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response