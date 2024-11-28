from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from shop.models import Product
from cart.models import Cart
from cart.models import Payment
from cart.models import Order_details

import razorpay
from django.http import HttpResponse
# Create your views here.
@login_required
def addtocart(request,i):
    p=Product.objects.get(id=i)
    u=request.user

    try:
        c=Cart.objects.get(product=p,user=u)
        if(p.stock>0):
            c.quantity+=1
            c.save()
            p.stock-=1
            p.save()
    except:
        if (p.stock > 0):
            c=Cart.objects.create(product=p,user=u,quantity=1)
            c.save()
            p.stock -= 1
            p.save()
    return redirect('cart:cart')
@login_required
def cartview(request):
    u=request.user
    try:
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total += i.quantity*i.product.price
        context = {'cart': c,'total':total}
    except:
        pass



    return render(request, 'cart.html',context)
@login_required
def cart_remove(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c=Cart.objects.get(product=p,user=u)

        if(c.quantity > 1):
            c.quantity -= 1
            c.save()
            p.stock+=1
            p.save()
        else:
            c.delete()
            p.stock+=1
            p.save()
    except:
        pass
    return redirect('cart:cart')
@login_required
def cart_del(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    c = Cart.objects.get(product=p, user=u)
    c.delete()
    p.stock += c.quantity
    p.save()
    return redirect('cart:cart')

def orderform(request):
        if(request.method=="POST"):
            addrss = request.POST['a']
            phno = request.POST['ph']
            pin = request.POST['p']
            u=request.user
            print(u)
            c = Cart.objects.filter(user=u)
            print(c)
            total=0
            for i in c:
                total += i.quantity*i.product.price
            total1 = int(total*100)
            print(u,"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            client=razorpay.Client(auth=('rzp_test_9nZMTHCIYf9u4w','MtxqAsvUfpoGNtk4RKuNpRm1'))
            response_payment=client.order.create(dict(amount=total1,currency="INR"))
            print(response_payment)
            order_id=response_payment['id']
            status=response_payment['status']
            if(status=="created"):
                p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
                p.save()
                for i in c:
                    o=Order_details.objects.create(product=i.product,user=u,no_of_items=i.quantity,address=addrss,phone=phno,pin=pin,order_id=order_id)
                    o.save()

            response_payment['name']=u.username
            context={'payment':response_payment}
            return render(request, 'payment.html',context)
        return render(request, 'billingdetails.html')
@csrf_exempt
def payment_status(request,u):
    usr = User.objects.get(username=u)
    print(usr)
    if not request.user.is_authenticated:
        login(request,usr)

    if(request.method=="POST"):
        response=request.POST
        print(response)

        param_dict = {
            "razorpay_order_id":response['razorpay_order_id'],
            "razorpay_payment_id": response['razorpay_payment_id'],
            "razorpay_signature": response['razorpay_signature'],
        }

        client=razorpay.Client(auth=('rzp_test_9nZMTHCIYf9u4w','MtxqAsvUfpoGNtk4RKuNpRm1'))
        print(client)
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)
            p=Payment.objects.get(order_id=response['razorpay_order_id'])
            p.razorpay_payment_id=response['razorpay_order_id']
            p.paid=True
            p.save()
            o=Order_details.objects.filter(order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="completed"
                i.save()
            usr = User.objects.get(user=u)
            c = Cart.objects.filter(user=usr)
            c.delete()

        except:
            pass

    return render(request, 'payment_status.html',{'status':status})

@login_required()
def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u)
    print(o)
    context={'orders':o}

    return render(request,'order_view.html',context)