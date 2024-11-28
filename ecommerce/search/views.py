from django.db.models import Q
from django.shortcuts import render
from shop.models import Product
# Create your views here.
def searchp(request):
    if (request.method=="POST"):
        query=request.POST['q']
        print(query)

        p=Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        context={'pro':p,'query':query}
    return render(request,'search.html',context)