import pickle
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.sessions.models import Session



def dashboard(request):
        
        session = Session.objects.get(session_key="2gadiqqn3ne85dcbz55enj3o0zh7dbng")
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return HttpResponse(user.username)
