from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction

def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions':transactions}
    return render(request,'tracker/transactions-list.html',context)