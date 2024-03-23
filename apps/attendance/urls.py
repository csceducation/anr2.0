from django.urls import path
from .views import (
   lab_attendance_for_batch,lab_attendance_form,add_update_lab_attendance,delete_lab_attendance,
   Theory_attendance_for_batch,Theory_attendance_form,add_update_Theory_attendance,delete_theory_attendance,
   daily_attendance_create,daily_attendance_list,daily_attendance_delete,daily_attendance_update,
   daily_staff_attendance_create,daily_staff_attendance_list,daily_staff_attendance_delete,daily_staff_attendance_update,
   dashboard,router
)
urlpatterns = [
   path("lab_attendance/<int:pk>/",lab_attendance_for_batch,name="lab_attendance"),
   path('lab_attendance_form/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',lab_attendance_form,name="lab_attendance_form"),
   path('delete_lab_attendance/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',delete_lab_attendance,name="delete_lab_attendance"),
   path('add_update_lab_attendance/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',add_update_lab_attendance,name="add_lab_attendance"),
   path("theory_attendance/<int:pk>/",Theory_attendance_for_batch,name="theory_attendance"),
   path('theory_attendance_form/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',Theory_attendance_form,name="theory_attendance_form"),
   path('delete_theory_attendance/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',delete_theory_attendance,name="delete_theory_attendance"),
   path('add_update_theory_attendance/batch/<int:batch_id>/date/<str:date>/session/<int:session>/',add_update_Theory_attendance,name="add_theory_attendance"),
   path('attendance/', router, name='router'),
   path('', daily_attendance_list, name='attendance_list'),
   path('create/', daily_attendance_create, name='attendance_create'),
   path('update/<int:pk>/', daily_attendance_update, name='attendance_update'),
   path('delete/<int:pk>/', daily_attendance_delete, name='attendance_delete'),
   path('staff', daily_staff_attendance_list, name='staff_attendance_list'),
   path('staff/create/', daily_staff_attendance_create, name='staff_attendance_create'),
   path('staff/update/<int:pk>/', daily_staff_attendance_update, name='staff_attendance_update'),
   path('staff/delete/<int:pk>/', daily_staff_attendance_delete, name='staff_attendance_delete'),
   path('dashboard/',dashboard,name="dashboard")
]