from django.urls import path
from . import views

urlpatterns = [
    path('lab/<int:batch_id>', views.lab_attendance, name='lab_attendance'),
    path('theory/<int:batch_id>', views.theory_attendance, name='theory_attendance'),
    path('staffs/day/', views.staff_attendance, name='staff_attendance'),
    path('students/day', views.student_attendance, name='student_attendance'),
    path('select/feature',views.router,name="router"),
    path('day_dashboard',views.day_dashboard,name="day_dashboard"),
    path('batch_dashboard/',views.batch_dashboard,name='batch_dashboard'),
]
