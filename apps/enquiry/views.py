import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import EnquiryForm, LogForm
from .models import Enquiry, Enquirylogs


class EnquiryListView(LoginRequiredMixin, ListView):
    model = Enquiry
    
    def slist(request):
        template_name = "enquiry.html"
        return render(request, template_name , context={"Enquiry":Enquiry.objects.all()})



class EnquiryDetailView(LoginRequiredMixin, DetailView):
    model = Enquiry
    template_name = "enquiry_details.html"

    def get_context_data(self, **kwargs):
        context = super(EnquiryDetailView, self).get_context_data(**kwargs)
        context["history"] = Enquirylogs.objects.filter(student=self.object)
        return context


class EnquiryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enquiry
    template_name = "enquiry_form.html"
    form_class = EnquiryForm
    success_message = "New Enquiry successfully added."

    def get_form(self, *args, **kwargs):
        form = super(EnquiryCreateView, self).get_form(*args, **kwargs)
        
        # Customize widget for the date field
        form.fields["enquiry_date"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["expected_date"].widget = widgets.DateInput(attrs={"type": "date"})
        
        # Customize widget for the address field
        form.fields["qualification"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        form.fields["studying_course"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        form.fields["counsellor_remark"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        return form



class EnquiryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Enquiry
    success_message = "Record successfully updated."
    form_class = EnquiryForm
    template_name = "enquiry_form.html"

    def get_form(self, *args, **kwargs):
        form = super(EnquiryUpdateView, self).get_form(*args, **kwargs)
        
        # Customize widget for the date field
        form.fields["enquiry_date"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["expected_date"].widget = widgets.DateInput(attrs={"type": "date"})
        
        # Customize widget for the address field
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        form.fields["qualification"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        form.fields["studying_course"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        form.fields["counsellor_remark"].widget = widgets.Textarea(attrs={"rows": 1,"cols":25})
        return form



class EnquiryDeleteView(LoginRequiredMixin, DeleteView):
    model = Enquiry
    success_url = reverse_lazy("enquiry-list")
    template_name="del_confirm.html"


class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="enquiry_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "enquiry_no",
                "name",
                "gender",
                "mobile_number",
                "address",
                "enquiry_statuss",
            ]
        )

        return response


class LogCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enquirylogs
    template_name = "history.html"
    form_class = LogForm
    success_message = "Log added."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        # Get the student ID from the URL parameter
        kwargs['initial'] = {'student': self.kwargs['pk']}

        return kwargs

    def get_success_url(self):
        # Redirect to the absolute URL of the related Enquiry instance
        return reverse_lazy('enquiry-detail', kwargs={'pk': self.object.student.pk})

def delete_enquiry_log(request, pk):
    enquiry_log = get_object_or_404(Enquirylogs, pk=pk)
    enquiry_log.delete()
    referring_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referring_url) 