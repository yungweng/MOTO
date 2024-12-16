
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('get_user_by_id/<int:id>/', views.UserDetailView.as_view(), name='user_detail_view'),
    path('get_user_list/', views.UserListView.as_view(), name='get_user_list'),
    path('get_room_list/', views.RoomListView.as_view(), name='get_room_list'),
    path('get_user_educational_specialist_without_supervision/', views.PersonalListView.as_view(), name='get_user_educational_specialist_without_supervision'),
    path('get_ag_categories_list/', views.AGKategorieListView.as_view(), name='get_ag_categories_list'),
    path('get_room_information/<int:raum_id>/', views.RaumDetailView.as_view(), name='get_room_information'),
    path('register_tablet_to_room/', views.RegisterTabletToRoom.as_view(), name='register_tablet_to_room'),
    path('unregister_tablet_from_room/', views.UnregisterTabletView.as_view(), name='unregister_tablet_from_room'),
    path('register_student_in_room/', views.RegisterStudentWithTabletView.as_view(), name='register_student_in_room'),
    path('unregister_student_from_room/', views.UnregisterStudentFromRoomView.as_view(), name='unregister_student_from_room'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('change_tag_id/', views.AssignTagIDView.as_view(), name='change_tag_id'),
    path('give_feedback/', views.FeedbackSubmissionView.as_view(), name='give_feedback'),
    path('authenticate/', views.AuthenticateUserView.as_view(), name='authenticate'),
    path('update_room/', views.UpdateRaumBelegungView.as_view(), name='update_room'),
    path('get_active_room_information/', views.GetRaumBelegungView.as_view(), name='get_active_room_information'),
    
]