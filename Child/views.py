from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth  import authenticate,  login, logout
from matplotlib.style import context
from numpy import product
from pkg_resources import require
from pytest import Instance
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required

from Child.form import *
from Child.models import *

# Create your views here.
def home(request):
    return render(request,"index.html")

@login_required(login_url='home')
def featurepage(request):
    return render(request,"featurepage.html")


def handleSignUp(request):

          if request.method=="POST":
               # Get the post parameters
               username=request.POST['username']
               email=request.POST['email']
               fname=request.POST['fname']
               lname=request.POST['lname']
               pass1=request.POST['pass1']
               pass2=request.POST['pass2']

               # check for errorneous input
               if len(username)<5:
                    messages.error(request, " Your user name must be under 5 characters")
                    return redirect('home')

               if not username.isalnum():
                    messages.error(request, " User name should only contain letters and numbers")
                    return redirect('/')
               if (pass1!= pass2):
                    messages.error(request, " Passwords do not match, try again please")
                    return redirect('/')
               
               # Create the user
               if User.objects.filter(username=username).first():
                         messages.error(request, "This username is already taken, try another for example: username123")
                         return redirect('/')

               myuser = User.objects.create_user(username,email,pass1)
               myuser.first_name= fname
               myuser.last_name= lname
               myuser.save()

               g = Group.objects.get(name='Customer')
               users = User.objects.filter(username=username)
               for u in users:
                g.user_set.add(u)

                Customer.objects.create(
				user=myuser,
				username=myuser.username,
				email=myuser.email,
                fname=myuser.first_name,
                lname=myuser.last_name,
				)

               messages.success(request, " Your account has been successfully created")
               return redirect('/')
        
          else:
               return HttpResponse("404 - Not found")

def handeLogin(request):

          if request.method=="POST":
               # Get the post parameters
               loginusername=request.POST['loginusername']
               loginpassword=request.POST['loginpassword']

               user=authenticate(username= loginusername, password= loginpassword)
               if user is not None:
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return render(request, 'featurepage.html')
               else:
                    messages.error(request, "Invalid credentials! Please try again")
                    return redirect("/")

          return HttpResponse("404- Not found")

def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


@login_required(login_url='home')
def profilepage(request):
     customer =request.user.customer
     form = CustomerForm(instance=customer)
     orders = request.user.customer.order_set.all()

     if request.method== 'POST':
          form=CustomerForm(request.POST, request.FILES, instance=customer)
          if form.is_valid():
               form.save()
     context ={'form':form,'orders':orders}
     return render(request,"profile.html",context)

def contactpage(request):
     if request.method == "POST":
          name = request.POST.get('name')
          email = request.POST.get('email')
          phone = request.POST.get('phone')
          desc = request.POST.get('desc')
          contact= Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
          contact.save()
          messages.success(request, 'Your message has been sent')
     return render(request,"contact.html")


@login_required(login_url='home')
def adminpage(request):
     c = Contact.objects.all()
     d = Daycare.objects.all()
     o = Order.objects.all()
     b = BkashPayment.objects.all()
     n = NagadPayment.objects.all()
     t_o = o.count()
     t_p = o.filter(status = 'pending').count()
     t_d = o.filter(status = 'delivered').count()
     if request.method == "POST":
          id_list = request.POST.getlist('boxes')

          #uncheck all events
          d.update(approved=False)
          #update the database
          for x in id_list:
               Daycare.objects.filter(pk=int(x)).update(approved=True)

     context = {'c':c,'d':d,'o':o,'b':b,'n':n,'t_o':t_o,'t_p':t_p,'t_d':t_d,}
     return render(request,"adminpage.html",context)


@login_required(login_url='home')
def helppage(request):
     c = request.user.id
     if request.method == "POST":
          childname = request.POST.get('childname')
          address = request.POST.get('address')
          contact = request.POST.get('contact')
          desc = request.POST.get('desc')
          account = request.POST.get('account')
          help= Help(childname=childname,address=address,contact=contact,desc=desc,account=account)
          help.save()
          messages.success(request, 'Your information is successfully generated')
     
     h = Help.objects.all()
     context= {'h':h}
     return render(request,"help.html",context)


@login_required(login_url='home')
def updatehelp(request, pk):

	help = Help.objects.get(id=pk)
	form = HelpForm(instance=help)

	if request.method == 'POST':
		form = HelpForm(request.POST, instance=help)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'order_form.html', context)


@login_required(login_url='home')
def deleteHelp(request, pk):
	help = Help.objects.get(id=pk) 
	if request.method == "POST":
		help.delete()
		return redirect('/help')

	context = {'help':help}
	return render(request, 'delete.html', context)


@login_required(login_url='home')
def deleteComments(request, pk):
	comment = Contact.objects.get(id=pk) 
	if request.method == "POST":
		comment.delete()
		return redirect('/adminpage')

	context = {'comment':comment}
	return render(request, 'delete.html', context)


@login_required(login_url='home')
def daycare(request):
     d = Daycare.objects.all()
     if request.method == "POST":
          organization_name = request.POST.get('organization_name')
          location = request.POST.get('location')
          service_time = request.POST.get('service_time')
          desc = request.POST.get('desc')
          daycare= Daycare(organization_name=organization_name,location=location,service_time=service_time,desc=desc)
          daycare.save()
          messages.success(request, 'Your information is successfully generated. Please wait for approval')

     context= {'d':d}
     return render(request,"daycare.html",context)


@login_required(login_url='home')
def addschool(request):
    a= Schooldetails.objects.all()
    form = SchoolForm()

    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Your information is Recorded")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form=SchoolForm()

    context={'form':form,'a':a}
    return render(request, 'school.html', context)

@login_required(login_url='home')
def schoolupdate(request, pk):
    school = Schooldetails.objects.get(id=pk)
    form = SchoolForm(instance=school)
    if request.method == 'POST':
        form = SchoolForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, " Your information is Updated")
            return redirect('/school')
    context = {'form':form}
    return render(request, 'order2_form.html', context) #may be lagbe na


@login_required(login_url='home')
def load_schools(request):
    district_id = request.GET.get('district_id') #It will fetch that address id.It comes from ajax.
    schools = School.objects.filter(district_id=district_id) #Filter the hospitals based on the address.
    return render(request, 'school_dropdown_list_options.html', {'schools': schools}) #After Rendering this HTML page, It will send response back to where it is being called 


@login_required(login_url='home')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product',))
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect(request.META.get('HTTP_REFERER'))

	context = {'form':formset}
	return render(request, 'order1_form.html', context)

@login_required(login_url='home')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('adminpage')

	context = {'form':form}
	return render(request, 'order_form.html', context)


@login_required(login_url='home')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/orderedlist')

	context = {'item':order}
	return render(request, 'delete.html', context)


@login_required(login_url='home')
def productpage(request):
     return render(request,'product.html')

@login_required(login_url='home')
def orderedpage(request):
     orders = request.user.customer.order_set.all()
     context ={'orders':orders}
     return render(request,'ordered_list.html',context)

def aboutpage(request):
     return render(request,'aboutpage.html')


def discussion(request,pk):
    room = Discussion.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('discussion', pk=room.id)

    context={'room':room, 'room_messages':room_messages,'participants': participants}
    return render(request, 'discussion.html',context)

def createDiscussion(request):
    form = DiscussionForm()
    topics = DiscussionTopic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = DiscussionTopic.objects.get_or_create(name=topic_name)
        Discussion.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            more=request.POST.get('more')
        )
        return redirect('/discussion_topic')

    context = {'form': form,'topics':topics}
    return render(request, 'discussion_form.html', context)

def updateDiscussion(request, pk):
    room = Discussion.objects.get(id=pk)
    form = DiscussionForm(instance=room)
    topics = DiscussionTopic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = DiscussionTopic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.more = request.POST.get('more')
        room.save()
        return redirect('/discussion_topic')

    context = {'form': form,'topics': topics,'room':room}
    return render(request, 'discussion_form.html', context)

def deleteDiscussion(request, pk):
    room = Discussion.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('/discussion_topic')
    return render(request, 'delete.html', {'obj': room})

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('/discussion_topic')
    return render(request, 'delete.html', {'obj': message})

def discussion_topicpage(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''

    topic = DiscussionTopic.objects.all()
    room = Discussion.objects.filter(topic__name__icontains=q)
    context={'room':room,'topic':topic}
    return render(request, 'discussion_topic.html',context)

def videopage(request):
    return render(request,"videopage.html")

def paymentpage(request):
    return render(request,"paymentpage.html")

def bkashpage(request):
    form = BForm()

    if request.method == 'POST':
        form = BForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Your Payment Information is Recorded")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form=BForm()

    context={'form':form,}
    return render(request,"bkashpage.html",context)

def Nagadpage(request):
    form = NForm()

    if request.method == 'POST':
        form = NForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Your Payment Information is Recorded")
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form=NForm()

    context={'form':form,}
    return render(request,"nagadpage.html",context)