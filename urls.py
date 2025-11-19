"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include                 # add this
from rest_framework import routers                    # add this
from dataccess import views   
from django.views.decorators.csrf import csrf_exempt                         # add this
# from rest_framework.authtoken import views

router = routers.DefaultRouter()                      # add this
# router.register(r'task', views.UserView, 'task')     # add this
# router.register(r'users', views.UserViewSet, 'users')

urlpatterns = [
    path('register/',views.RegisterUser.as_view()), # able to register a new user, while some user is logged in or logged out
    path('exercise/', views.exercise_list),
    # path('exercise/', views.DoctorExerciseList.as_view()), # create exercise using doctor login
    path('exercise/<int:pk>', views.exercise_detail), # not used
    path('treatment/', views.treatment_list),
    path('treatment/list/',views.treatment_list2),
    path('create/doctor/', views.CreateDoctor.as_view()),
    path('create/staff/', views.CreateStaff.as_view()),
    path('create/patient/', views.CreatePatient.as_view()),
    path('login/', views.LoginView.as_view()),
    path('login/patient/treatments/', views.treatment_listPatient),
    path('login/patient/<int:treatId>/', views.treatment_patient), #getTreatmentId
    path('login/patient/relatives/', views.relatives_list),
    path('create/notification/',views.create_notification),
    path('login/patient/notifications/', views.notification_list),
    path('create/record/', views.create_record),
    path('login/doctor/<int:treatId>/', views.treatment_doctor),
    path('login/user/<int:userId>/',views.detail),
    # path('api-token-auth', views.obtain_auth_token)
    # path('login/',views.LoginView.as_view(),name="login"),
    # path('register/', views.CreateUserView.as_view(), name='user'),
    # path('register/', views.UserViewSet, name='register'),
    # path('task/', views.LoginView.as_view(), name='task'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('faculty/<int:facId>/courses',views.FacultiesCoursesView.as_view(),name="faculty-courseoffered"),
    # path('student/<int:stuId>/courses',views.StudentsCoursesView.as_view(),name="student-coursesregistered"),
    path('', include(router.urls)),
]