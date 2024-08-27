# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from TestApp.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('testapp/', include('TestApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Исправлено
    path('test_page/', test_page, name='test_page'),
    path('do_pass_test/<int:id_of_test>/', do_pass_test, name='do_pass_test'),  # Добавлен слэш
    path('get_next_question/<int:num_of_question>/', get_next_question, name='get_next_question'),
    path('end_test/', end_test, name='end_test'),
    path('', home, name='home'),
]