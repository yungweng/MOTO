from datetime import datetime
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect

from main_app.view.choose_room.choose_room_view import choose_room_view
from main_app.view.create_activity.create_activity_view import create_activity_view
from main_app.view.csv_import.csv_import_view import csv_import_view
from main_app.view.change_roomdata.change_roomdata_view import change_roomdata_view
from main_app.view.remove_tablet.remove_tablet_view import remove_tablet_view
from main_app.view.user_verification.login_view import login_view
from main_app.view.user_verification.logout_view import logout_view
from main_app.view.user_verification.su_pw_reset_view import su_pw_reset_view
from main_app.view.user_verification.set_new_password_view import set_new_password_view
from main_app.view.user_verification.reset_pw_confirmation_view import reset_pw_confirmation_view
from main_app.view.pupil.pupil_view import pupil_view
from main_app.view.ogs_group.ogs_group_view import ogs_group_view
from main_app.view.room.select_room_view import select_room_view
from main_app.view.room.room_selection_view import room_selection_view
from main_app.view.room.room_information_view import room_information_view
from main_app.view.preferences.preferences_view import preferences_view
from main_app.view.master_android.master_android_view import master_android_view
from main_app.view.master_web.master_web_view import master_web_view
from main_app.view.room.room_usage_history_view import room_usage_history_view
from main_app.view.home.home_view import home_view
from main_app.view.set_nfc_set.set_nfc_set_view import set_nfc_set_view
from main_app.view.nfc_login.checked_out_view import checked_out_view
from main_app.view.nfc_login.go_home import go_home_view
from main_app.view.nfc_login.checked_in_view import checked_in_view
from main_app.view.nfc_login.leave_room_view import leave_room_view
from main_app.view.history_pages_students.room_history_view import room_history_view
from main_app.view.history_pages_students.feedback_history_view import feedback_history_view
from main_app.view.set_nfc_scan.set_nfc_scan_view import set_nfc_scan_view
from main_app.view.search_pupil.search_pupil import search_pupil_view
from main_app.view.dashboard.dashboard_view import dashboard_view
from main_app.view.history_pages_students.food_history import food_history_view
from main_app.view.representation.representation import representation_view
from main_app.view.change_data_db.choose_data_view import choose_data_view
from main_app.view.change_data_db.select_student_view import select_student_change_view
from main_app.view.change_data_db.select_group_view import select_group_change_view
from main_app.view.change_data_db.select_pa_view import select_pa_change_view
from main_app.view.change_data_db.select_room_view import select_room_change_view

def master_web(request):
    return master_web_view(request)

def master_android(request):
    return master_android_view(request)

def remove_tablet(request):
    return remove_tablet_view(request)

class SetNfcScanAndroidView(TemplateView):
    template_name = 'master_android/set_nfc_scan.html'

def choose_room(request):
    return choose_room_view(request)

def create_activity(request, raum):
    return create_activity_view(request, raum)

def csv_import(request):
    return csv_import_view(request)

def change_roomdata(request):
    return change_roomdata_view(request)

def login(request):
    return login_view(request)

def logout(request):
    return logout_view(request)

def superuser(request):
    return su_pw_reset_view(request)

def set_new_pw(request):
    return set_new_password_view(request)

def reset_pw_confirmation(request):
    return reset_pw_confirmation_view(request)

def pupil(request, pupil):
    return pupil_view(request, pupil)

def ogs_group(request):
    return ogs_group_view(request)

def select_room(request):
    return select_room_view(request)

def room_selection(request, raum):
    return room_selection_view(request,raum)

def room_information (request, raum):
    return room_information_view(request,raum)

def preferences(request):
    return preferences_view(request)

def room_usage_history(request, raum):
    return room_usage_history_view(request, raum)

def home(request):
    return home_view(request)

def set_nfc_set(request):
    return set_nfc_set_view(request)

def checked_out(request):
    return checked_out_view(request)

def go_home(request):
    return go_home_view(request)

def go_home_feedback(request, feedback):
    return go_home_view(request, feedback)

def checked_in(request):
    return checked_in_view(request)

def leave_room(request):
    return leave_room_view(request)

def room_history(request, pupil):
    return room_history_view(request,pupil)

def feedback_history(request, pupil):
    return feedback_history_view(request,pupil)

def set_nfc_scan(request):
    return set_nfc_scan_view(request)

def search_pupil(request):
    return search_pupil_view(request)

def dashboard(request):
    return dashboard_view(request)

def food_history(request, pupil):
    return food_history_view(request,pupil)

def representation(request):
    return representation_view(request)

def choose_data(request):
    return choose_data_view(request)

def select_student_change(request):
    return select_student_change_view(request)

def select_room_change(request):
    return select_room_change_view(request)

def select_pa_change(request):
    return select_pa_change_view(request)

def select_group_change(request):
    return select_group_change_view(request)