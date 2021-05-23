from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

def home_page(request):    
    if request.method == 'POST':
        # creates new object and saves it
        Item.objects.create(text=request.POST['item_text'])
        # always redirect after post request
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
