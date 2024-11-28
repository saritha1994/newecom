from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from shop.models import Category
from shop.models import Product
# Create your views here.
def categories(request):
    c=Category.objects.all()
    context={'cat':c}
    return render(request,'categories.html',context)

def addcategory(request):
    if(request.method=="POST"):
        n=request.POST['n']
        d = request.POST['d']
        i = request.FILES['i']
        c=Category.objects.create(name=n,image=i,description=d)
        c.save()
        return redirect('shop:category')
    return render(request, 'addcategories.html')

def addproducts(request):
    if(request.method=="POST"):
        n=request.POST['n']
        d = request.POST['d']
        i = request.FILES.get('i')
        s = request.POST['s']
        p = request.POST['p']
        c = request.POST['c']
        cat=Category.objects.get(name=c)
        x = Product.objects.create(name=n,image=i,description=d,stock=s,price=p,category=cat)
        x.save()
        return redirect('shop:category')
    return render(request, 'addproducts.html')
# def products(request,p):
#     k = Category.objects.get(id=p)
#     context = {'cat': k}
#     return render(request,'products.html',context)

def products(request,p):
    c = Category.objects.get(id=p)
    p = Product.objects.filter(category=c)
    context = {'cat': c ,'pro': p}
    return render(request, 'products.html', context)

def productdetail(request,p):
    p = Product.objects.get(id=p)
    context = {'pro':p}
    return render(request, 'productdetail.html', context)

def registration(request):
    if (request.method == "POST"):
        U = request.POST['un']
        p = request.POST['p']
        c = request.POST['cp']
        f = request.POST['f']
        l = request.POST['l']
        e = request.POST['e']
        if (p == c):
            u = User.objects.create_user(username=U, password=p, email=e, first_name=f, last_name=l)
            u.save()
            # return HttpResponse("pooding")
            return redirect('shop:login')
        else:
            return HttpResponse("password is not same")
    return render(request, 'registration.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST["un"]
        p = request.POST["p"]
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('shop:category')
        else:
            return HttpResponse("invalid credentials")
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'login.html')

def addstock(request,p):
    product=Product.objects.get(id=p)
    context={'pro':product}
    if(request.method=="POST"):
        product.stock=request.POST['n']
        product.save()
        return redirect('shop:productdetail',p)

    return render(request, 'addstock.html',context)

