import datetime

from django.db.models import F, Sum
from django.shortcuts import render

from ..finance import models as finmod
from ..students import models as stumod


def total_student():
    total_stud = stumod.Student.objects.count()
    totals = total_stud
    return totals

def total_income():
    total_am = finmod.Invoice.objects.all()
    total_ammount = sum(account.total_amount_payable() for account in total_am)
    return total_ammount

def total_paid():
    total_pa = finmod.Receipt.objects.all()
    total_pait = total_pa.aggregate(total=Sum('amount_paid'))['total']
    return total_pait

def total_balance():
    total_bal = finmod.Invoice.objects.all()
    total_balanc = sum(account.balance() for account in total_bal)
    return total_balanc


#------------------------------------------------------------------------------

def today_income(request):
    global total_col
    date = datetime.date.today()
    rec = finmod.Receipt.objects.filter(date_paid = date)
    total_col = rec.aggregate(total=Sum('amount_paid'))['total']
    return render(request ,"today.html",context={
        "recipt":rec,
        "date":date,
        "today_col":total_col
    })
def month_income(request):
    month = request.GET.get('month')
    month1 = datetime.datetime.now().month
    rec = finmod.Receipt.objects.filter(date_paid__month = month or month1)
    total_col = rec.aggregate(total=Sum('amount_paid'))['total']
    return render(request ,"month.html",context={
        "recipt":rec,
        "today_col":total_col
    })
def all_income(request):
    rec = finmod.Receipt.objects.all()
    total_col = rec.aggregate(total=Sum('amount_paid'))['total']
    return render(request ,"revenue.html",context={
        "recipt":rec,
        
        "today_col":total_col
    })