import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect

from myhome.forms import SearchDateForm

def home(request):

    if request.method == 'POST':
        form = SearchDateForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            date = form.cleaned_data['search_date']
            date = date.strftime('%Y-%m-%d')
            return redirect('/'+date)

        else:
            date = datetime.date.today()

    else:
        date = datetime.date.today()
        form = SearchDateForm(initial={'search_date': date})

    context = {
    'form': form,
    'date': date,
    }

    return render(request, 'myhome/home.html', context)

def search(request, date):
    context = {'date': date,}
    return render(request, 'myhome/search.html', context)
