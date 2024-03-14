from django.urls import path

from .views import (
    DownloadCSVViewdownloadcsv,
    EnquiryCreateView,
    EnquiryDeleteView,
    EnquiryDetailView,
    EnquiryListView,
    EnquiryUpdateView,
    LogCreateView,
    delete_enquiry_log,
)

urlpatterns = [
    path("list",EnquiryListView.slist, name="enquiry-list"),
    path("<int:pk>/histroy",LogCreateView.as_view(),name="logview"),
    path("<int:pk>/",EnquiryDetailView.as_view(), name="enquiry-detail"),
    path("create/",EnquiryCreateView.as_view(), name="enquiry-create"),
    path("<int:pk>/update/",EnquiryUpdateView.as_view(), name="enquiry-update"),
    path("delete/<int:pk>/",EnquiryDeleteView.as_view(), name="enquiry-delete"),
     path("endelete/<int:pk>/", delete_enquiry_log, name="enhis-delete"),
    path("download-csv/", DownloadCSVViewdownloadcsv.as_view(), name="download-csv"),
]
