from django.urls import path
from django.views.generic import RedirectView
from . import views



urlpatterns = [
    # View paths:
    path('master_web/', views.master_web, name='master_web'),
    path('master_tablet/', views.master_android, name='master_tablet'),
    path('remove_tablet/', views.remove_tablet, name='remove_tablet'),
    path('choose_room/', views.choose_room, name='choose_room'),
    path('create_activity/<str:raum>', views.create_activity, name='create_activity'),
    path('csv_import/', views.csv_import, name='csv_import'),
    path('change_roomdata/', views.change_roomdata, name='change_roomdata'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('superuser/', views.superuser, name='superuser'),
    path('set_new_pw/', views.set_new_pw, name='set_new_pw'),
    path('reset_pw_confirmation/', views.reset_pw_confirmation, name='reset_pw_confirmation'),
    path('pupil/<int:pupil>', views.pupil, name='pupil'),
    path('ogs_group/', views.ogs_group, name='ogs_group'),
    path('select_room/', views.select_room, name='select_room'),
    path('room_selection/<str:raum>', views.room_selection, name='room_selection'),
    path('room_information/<str:raum>', views.room_information, name='room_information'),
    path('preferences/', views.preferences, name='preferences'),
    path('room_usage_history/<str:raum>', views.room_usage_history, name='room_usage_history'),
    path('home/', views.home, name='home'),
    path('set_nfc_set/', views.set_nfc_set, name='set_nfc_set'),
    path('checked_out/', views.checked_out, name='checked_out'),
    path('go_home/', views.go_home, name='go_home'),
    path('go_home/<str:feedback>', views.go_home_feedback, name='go_home_feedback'),
    path('checked_in/', views.checked_in, name='checked_in'),
    path('leave_room/', views.leave_room, name='leave_room'),
    path('room_history/<int:pupil>', views.room_history, name='room_history'),
    path('feedback_history/<int:pupil>', views.feedback_history, name='feedback_history'),
    path('set_nfc_scan/', views.set_nfc_scan, name='set_nfc_scan'),
    path('search_pupil/', views.search_pupil, name='search_pupil'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('food_history/<int:pupil>', views.food_history, name='food_history'),
    path('representation/', views.representation, name='representation'),
    path('choose_data/', views.choose_data_view, name='choose_data'),
    path('choose_data/student/', views.select_student_change_view, name='choose_data_student'),
    path('choose_data/room/', views.select_room_change, name='choose_data_room'),
    path('choose_data/pa/', views.select_pa_change, name='choose_data_pa'),
    path('choose_data/group/', views.select_group_change, name='choose_data_group'),
    path('choose_data/student/<int:id>', views.change_student, name='change_student_data'),
    path('choose_data/room/<int:id>', views.change_room, name='change_room_data'),
    path('choose_data/group/<int:id>', views.change_student, name='change_group_data'),
    path('choose_data/pa/<int:id>', views.change_student, name='change_pa_data'),
]


allowed_urls_android = [
    'master_tablet',
    'remove_tablet',
    'set_nfc_scan',
    'choose_room',
    'create_activity',
    'change_roomdata',
    'login',
    'logout',
    'set_new_pw',
    'home',
    'set_nfc_set',
    'checked_out',
    'go_home',
    'go_home_feedback',
    'checked_in',
    'leave_room',
    'set_nfc_scan',
    'reset_pw_confirmation',
    ]
main_url_android = 'master_tablet'

allowed_urls_android_no_room = [
    'choose_room',
    'create_activity',
    ]
main_url_android_no_room = 'choose_room'

allowed_urls_web = [
    'master_web',
    'csv_import',
    'login',
    'logout',
    'superuser',
    'set_new_pw',
    'reset_pw_confirmation',
    'pupil',
    'ogs_group',
    'select_room',
    'room_selection',
    'room_information',
    'preferences',
    'room_usage_history',
    'room_history',
    'feedback_history',
    'search_pupil',
    'dashboard',
    'food_history',
    'representation',
    'choose_data',
    'choose_data_student',
    'choose_data_pa',
    'choose_data_room',
    'choose_data_group',
    'change_student_data',
    'change_room_data',
    'change_pa_data',
    'change_group_data',
    ]
main_url_web = 'master_web'

urls_apis = [

    'api_test',

]