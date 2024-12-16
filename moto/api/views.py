from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from api.view.user.get_user_by_id_api import UserDetailView
from api.view.user_verification.logout_api import LogoutView
from api.view.user.get_user_list import UserListView
from api.view.room.get_rooms_list import RoomListView
from api.view.user.get_user_educational_specialist_without_supervision import PersonalListView
from api.view.ag.get_ag_categories import AGKategorieListView
from api.view.room.get_room_information import RaumDetailView
from api.view.user_verification.login_api import LoginView
from api.view.room.register_room_api import RegisterTabletToRoom
from api.view.room.unregister_room_api import UnregisterTabletView
from api.view.room.register_student_in_room import RegisterStudentWithTabletView
from api.view.room.unregister_student_from_room import UnregisterStudentFromRoomView
from api.view.user_verification.change_password import ChangePasswordView
from api.view.user.change_tag_id import AssignTagIDView
from api.view.user.give_feedback import FeedbackSubmissionView
from api.view.user_verification.authenticate_user import AuthenticateUserView
from api.view.room.update_room import UpdateRaumBelegungView
from api.view.room.get_active_room_information import GetRaumBelegungView


# Beispiel für Geschützte Route
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Beispielroute, die nur für authentifizierte Nutzer zugänglich ist.
        """
        return Response({"message": f"Hallo {request.user.username}, dies ist eine geschützte Route!"})