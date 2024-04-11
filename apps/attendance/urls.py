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
    path("delete_lab_attendance/<int:batch_id>/<str:date>/<int:stud_id>/",views.delete_lab_attendance,name="delete_lab_attendance"),
    path("delete_theory_attendance/<int:batch_id>/<str:date>/<int:stud_id>/",views.delete_theory_attendance,name="delete_theory_attendance"),
    path("delete_staff_attendance/<str:date>/<int:staff_id>/",views.delete_staff_attendance,name="delete_staff_attendance"),
    path("delete_student_attendance/<str:date>/<int:student_id>/",views.delete_student_attendance,name="delete_student_attendance")
]
