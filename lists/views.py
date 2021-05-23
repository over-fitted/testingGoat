from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

def home_page(request):    
    if request.method == 'POST':
        # creates new object and saves it
        Item.objects.create(text=request.POST['item_text'])
        # always redirect after post request
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


