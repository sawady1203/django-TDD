# lists/views.py

# from django.shortcuts import HttpResponse
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        print(request)
        print(request.POST)
        print(request.POST['item_text'])
        print(request.POST.get('item_text', ''))
        return render(request, 'lists/home.html', {
            'new_item_text': request.POST['item_text'],
        })
    return render(request, 'lists/home.html')
