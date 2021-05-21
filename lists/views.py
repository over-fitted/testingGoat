from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    # second arg = which template to return
    # third arg = dict binding variables to vals
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
        # .get instead of ['item_text] to supply default value as second arg
    })
