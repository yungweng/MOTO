from api.view.login.login_api import login_api
from api.view.user.get_user_by_id_api import UserDetailView
from api.view.rooms.choose_room import get_rooms_api

def login(request):
    return login_api(request)

# add choose room api
def get_rooms(request):
    return get_rooms_api(request)

# def get_user_by_id(request, id):
#     return get_user_by_id_api(request, id)
