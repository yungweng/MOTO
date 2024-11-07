from api.view.login.login_api import login_api
from api.view.user.get_user_by_id_api import UserDetailView

def login(request):
    return login_api(request)

# def get_user_by_id(request, id):
#     return get_user_by_id_api(request, id)

