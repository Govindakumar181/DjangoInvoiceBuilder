from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login,authenticate,logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage

from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

@login_required(login_url='signin')
def index(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        context={
            'profile':profile,
            'active1':'active-menu',
        }  
        return render(request, 'payment/index.html', context)
    else:
        return render(request, 'payment/index.html', {})
        # return HttpResponse('Error')

@login_required(login_url='signin')
def customers(request):

    if 'customer_submit' in request.POST:
        if request.method == 'POST':
            # customer_name = request.POST.get('customer_name')
            # customer_email = request.POST.get('customer_email')
            # customer_project_title = request.POST.get('customer_project_title')
            # total_cost = request.POST.get('total_cost')
            # milestone = request.POST.get('milestone')
            # start_date = request.POST.get('start_date')
            # due_date = request.POST.get('due_date')
            form = formCustomer(request.POST, request.FILES) 
            if form.is_valid(): 
                form.save() 
                return redirect('customers') 
            else:
                return redirect('index')

    customer = Customer.objects.all()

    paginator=Paginator(customer,10)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1

    try:
        customer=paginator.page(page)
    except(EmptyPage,InvalidPage):
        customer=paginator=paginator.page(paginator.num_pages)

    context = {
        'customer':customer,
        'active2':'active-menu',
    }
    return render(request, 'payment/customers.html', context)

@login_required(login_url='signin')
def viewcustomers(request,id):
    customer = Customer.objects.get(id=id)
    context={
        'customer':customer,
    }
    return render(request, 'payment/viewcustomers.html', context)

@login_required(login_url='signin')
def editcustomers(request,id):
    customer = Customer.objects.get(id=id)
    if 'customer_submit' in request.POST:
        if request.method == 'POST':
            # customer_name = request.POST.get('customer_name')
            # customer_email = request.POST.get('customer_email')
            # customer_project_title = request.POST.get('customer_project_title')
            # total_cost = request.POST.get('total_cost')
            # milestone = request.POST.get('milestone')
            # start_date = request.POST.get('start_date')
            # due_date = request.POST.get('due_date')
            form = formCustomer(request.POST, request.FILES,instance=customer) 
            if form.is_valid(): 
                form.save() 
                return redirect('customers') 
            else:
                return redirect('index')
    context={
        'customer':customer,
    }
    return render(request, 'payment/editcustomers.html', context)

@login_required(login_url='signin')
def deletecustomers(request,id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('customers')


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None
def downloadPDF(request, id):
    customer = Customer.objects.get(id=id)
    context = {
        'customer':customer,
        'time':datetime.now(),
        }
    # return render(request, 'payment/download_pdf.html', context)
    pdf = render_to_pdf('payment/download_pdf.html', context)
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Invoice_%s.pdf" %("12341231")
    content = "attachment; filename=%s" %(filename)
    response['Content-Disposition'] = content
    return response

@login_required(login_url='signin')
def copylink(request,id):
    customer = Customer.objects.get(id=id)

    context={'customer':customer}
    return render(request,'payment/payment.html',context)

import stripe
stripe.api_key = "sk_test_51J876GAkgNoo3fJpfgYYziA1lYbSFcowY5TU7FljwG16rOfUVerV6lqp5ge27E4nbwZYH34CsUvpRa4gPt9TWLPg00r2Q04i1L"
from django.urls import reverse
def charge(request):
    amount = 5
    if request.method == "POST":
        print("Data",request.POST)
        # amount = int(request.POST['amount'])

        customer = stripe.Customer.create(
			# email=request.POST['email'],
			# name=request.POST['nickname'],
			source=request.POST['stripeToken']
			)

        charge = stripe.Charge.create(
			customer=customer,
			amount=amount*100,
			currency='usd',
			description="Donation"
			)
        # print("Data1: ",charge)
        # print("Data3: ",charge["paid"])
        # stripe.confirmCardPayment(clientSecret).then(function(response) {
        # if charge.error:
        #     print(charge.error)
        if charge.payment_intent and charge.paymentIntent.status == 'succeeded':
            print("payment sahi hue h or paise bhi agaey")
        # elif charge.error:
        #     print("1: ",charge.error)
        else:
            print("payment nh hue h or paise bhi nh ay")
    
    return redirect(reverse('success',args=[amount]))
def successMesg(request,args):
    amount = args
    return render(request, 'payment/success.html',{'amount':amount})

@login_required(login_url='signin')
def search(request):
    query=request.GET['query']
    if len(query)>100:
        # allPosts=[]
        customer=Customer.objects.none()
    else:
        Customer_customer_name = Customer.objects.filter(customer_name__icontains=query)
        # Customercontent = Customer.objects.filter(content__icontains=query)
        # Customerslug = Customer.objects.filter(slug__icontains=query)

        customer = Customer_customer_name
        # customer=Customertitle.union(Customercontent,Customerslug)
    # if customer.count() == 0:
    #     # messages.error(request,"No search results found plear search with another query")
    #     return HttpResponse("Error")

    context={'customer':customer,'query':query}
    return render(request,'payment/search.html',context)

@login_required(login_url='signin')
def projects(request):
    context = {
        'active3':'active-menu',
    }
    return render(request, 'payment/projects.html', context)

@login_required(login_url='signin')
def tasks(request):
    context = {
        'active4':'active-menu',
    }
    return render(request, 'payment/tasks.html', context)

@login_required(login_url='signin')
def catalog(request):
    context = {
        'active7':'active-menu',
    }
    return render(request, 'payment/catalog.html', context)

@login_required(login_url='signin')
def salesReport(request):
    context = {
        'active5':'active-menu',
    }
    return render(request, 'payment/salesReport.html', context)

@login_required(login_url='signin')
def salesAPI(request):
    context = {
        'active6':'active-menu',
    }
    return render(request, 'payment/salesAPI.html', context)

@login_required(login_url='signin')
def salesSlab(request):
    context = {
        'active8':'active-menu',
    }
    return render(request, 'payment/salesSlab.html', context)

def signin(request):
    if request.user.is_authenticated:
            return redirect('index')
    else:
        if request.method =='POST':
            loginusername = request.POST['username']
            loginpassword = request.POST['password']   

            user = authenticate(request,username=loginusername,password=loginpassword)
            # if True:
                # if user.is_active:
            try:
                if User.objects.get(username=loginusername).is_active == True:
            #     my_user = User.objects.get(last_name=verify[0])
                    try:
                        login(request,user)
                        # messages.success(request,'Your Account has been Successfully logged in')
                        return redirect('index')
                    except:
                        # messages.error(request,'Your username or password might be incorrect.')
                        return redirect('signin')

            except User.DoesNotExist:
                # messages.error(request,'Your username or password might be incorrect.')
                return redirect('signup')
        return render(request,'accounts/signin.html',{})

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method =='POST':
            username = request.POST['username']
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            number = request.POST['number']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']

            # if not username.isalnum():
            #     # messages.error(request,'Your username is invalid. Your username should have alphanumeric characters e.g. John123')
            #     return redirect('signup')
            if len(username)>20:
                # messages.error(request,'Your username is invalid')
                return redirect('signup')
            if len(pass1)<8:
                # messages.error(request,'Your password must have at least 8 characters')
                return redirect('signup')
            if pass1 != pass2:
                # messages.error(request,'Your password do not match')
                return redirect('signup')
            if pass1==pass2:
                if(User.objects.filter(username=username).exists()):
                    # messages.error(request,"Username already exists")
                    return redirect('signup')
                elif(User.objects.filter(email=email).exists()):
                    # messages.error(request,"Email already exists")
                    return redirect('signup')
                elif(User.objects.filter(last_name=number).exists()):
                    # messages.error(request,"Contact number already exists")
                    return redirect('signup')
                else: 
                    myuser=User.objects.create_user(username,email,pass1)
                    if myuser:
                        myuser.first_name=fname
                        myuser.last_name=lname
                        myuser.save()
                        # messages.error(request,'Error while setting up your account. Please try again')      
                        return redirect('signin')
        else: 
            return render(request,'accounts/signup.html',{})
        return render(request,'account/signup.html',{'activeclass5':'activeclass5'})

def handlelogout(request):
    logout(request)
    return redirect('index')