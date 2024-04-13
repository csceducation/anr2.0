from django.db import models
from django.urls import reverse
from django.utils import timezone
from apps.staffs.models import Staff
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass
from apps.students.models import Student
import json

class Invoice(models.Model):
    total_num = 0
    student = models.ForeignKey(Student, on_delete=models.CASCADE,default=None)
    status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

    class Meta:
        ordering = ["student"]

    def __str__(self):
        return f"{self.student}"

    def balance(self):
        payable = self.total_amount_payable()
        paid = self.total_amount_paid()
        return payable - paid

    def amount_payable(self):
        items = InvoiceItem.objects.filter(invoice=self)
        total = 0
        for item in items:
            total += item.amount
        return total

    def total_amount_payable(self):
        return  self.amount_payable()

    def total_amount_paid(self):
        receipts = Receipt.objects.filter(invoice=self)
        amount = 0
        for receipt in receipts:
            amount += receipt.amount_paid
        return amount

    def get_absolute_url(self):
        return reverse("invoice-detail", kwargs={"pk": self.pk})


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()


class Receipt(models.Model):
    Bill_No = models.CharField(max_length=245 , default=None)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)
    received_by = models.ForeignKey(Staff,verbose_name="Billing Staff",on_delete=models.DO_NOTHING)
    def stats(self):
        return self.invoice.student.current_status
    def current_cls(self):
        return self.invoice.student.course
    def regno(self):
        return self.invoice.student.enrol_no
    def name(self):
        return self.invoice.student.student_name
    def __str__(self):
        return f"Receipt on {self.date_paid}"
    
    def save(self,due,date,*args,**kwargs):
        if due == None:
            self.save()
        else:
            dues = Due.objects.get(id=due)
            dues_list = dues.dues
            for item in dues_list:
                if item['date'] == date:
                    item['status'] = "paid"
            dues.dues = dues_list
            dues.save()
            super().save(*args, **kwargs)

class Due(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='due_invoice', on_delete=models.DO_NOTHING)
    total_amount = models.IntegerField()
    dues = models.JSONField(default=list)

    def extend_due(self,index,new_date,*args,**kwargs):
        due = self.dues[index]
        due['date'] = new_date

        self.dues[index] = due
        super().save(*args, **kwargs)



from django.db import connection

# Get the current date
current_date = "2024-04-13"
from django.db.models import Q
import json

# Fetch all Due objects
all_dues = Due.objects.all()

# List to store filtered dues
filtered_dues = []

# Iterate through each Due object
for due in all_dues:
    # Convert the JSON string to a Python object
    dues_list = json.loads(due.dues)

    # Iterate through each item in the dues list
    for item in dues_list:
        # Check if 'date' key exists in the item and if its value matches the current date
        if 'date' in item and item['date'] == str(current_date):
            # If it matches, add the Due object to the filtered list
            filtered_dues.append(due)

# Now filtered_dues contains Due objects where any of the JSON items has the current date
print(filtered_dues)