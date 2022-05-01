from.email import send_join_email
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django .contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse,Http404,HttpResponseRedirect, JsonResponse
from collect.forms import EventAttendForm,postProjectForm,ReviewForm,NewUserForm
from django.contrib import messages
from rest_framework import status
from rest_framework.parsers import JSONParser
from collect.serializers import EventSerializer
from rest_framework.decorators import api_view
from collect.models import Events, EventsAttendants,Post,Rating,ReviewRating

# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        messages.error(request,"registration Failed invalid credentials")
    form = NewUserForm()
    return render(request=request,template_name='registration/register.html',context={"register_form":form})

def login_user(request):
    if request.method =='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"invalid uername or password")
    form = AuthenticationForm()
    return render(request=request,template_name="registration/login.html",context={"login_form":form})

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login')
def current_events(request):
    events = Events.objects.all()
    attendes = EventsAttendants.objects.all()
    return render(request,'all-garbage/events.html',{"events":events,"attendes":attendes})

@login_required(login_url='login')
def attend_event(request):
    attendes = EventsAttendants.objects.all()
    if request.method == 'POST':
        form = EventAttendForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            recepient = EventsAttendants(name=name,email=email)
            recepient.save()
            send_join_email(name,email)
            HttpResponseRedirect('attend')
    else:
        form = EventAttendForm()
    return render(request,'all-garbage/attend.html',{"attendForm":form,"attendes":attendes})

@login_required(login_url='login')
def service(request):
    return render(request,'all-garbage/service.html')

@login_required(login_url='login')
def new_post(request):
    current_user = request.user
    if request.method == 'POST':
        form = postProjectForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = current_user
            article.save()
        return redirect('post')
    else:
        form = postProjectForm()
    return render(request, 'all-garbage/new-post.html', {"form": form})

@login_required(login_url='login')    
def posts(request):
    posts = Post.display_post()
    return render(request, 'all-garbage/post.html',{"posts": posts})

@login_required(login_url='login')
def view_post(request,id):
    project = Post.objects.get(id=id)
    rate = Rating.objects.filter( project=project).first()
    ratings = Rating.objects.all()
    rating_status = None
    if rate is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            review = Rating()
            review.project = project
            review.weight = weight
            review.total = (
                review.weight * 2 )
            review.save()
            return HttpResponseRedirect(reverse('view_project', args=(project.id,)))
    else:
        form = ReviewForm()
    params = {
        'project': project,
        'form': form,
        'rating_status': rating_status,
        'reviews': ratings,
        'ratings': rate
    }
    return render(request, 'all-garbage/view-post.html', params)
    
@login_required(login_url='login')
def submit_review(request, post_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, post__id=post_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.post_id = post_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
def logout_user(request):
    logout(request)
    messages.info(request,"Logged out successfully")
    return redirect('home')
    














@api_view(['GET','POST','DELETE'])
def event_list(request):
    if request.method == 'GET':
        events = Events.objects.all()
        name = request.GET.get('titile',None)
        if name is not None:
            events = Events.filter(name__icontains=name)

        events_serializer = EventSerializer(events,many=True)
        return JsonResponse(events_serializer.data,safe=False)
    elif request.method == 'DELETE':
        count = Events.objects.all().delete()
        return JsonResponse({'message': '{} events were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def event_details(request,pk):
    try:
        events = Events.objects.get(pk=pk)
    except Events.DoesNoExists:
        return JsonResponse({'message':'Events not existing'},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        event_serializer = EventSerializer(events)
        return JsonResponse(event_serializer.data)
    elif request.method == 'PUT':
        event_data = JSONParser().parse(request) 
        event_serializer = EventSerializer(events, data=event_data) 
        if event_serializer.is_valid(): 
            event_serializer.save() 
            return JsonResponse(event_serializer.data) 
        return JsonResponse(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        events.delete() 
        return JsonResponse({'message': 'event was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def event_list_published(request):
       events = Events.objects.filter(published=True)
       if request.method == 'GET': 
           events_serializer = EventSerializer(events, many=True)
           return JsonResponse(events_serializer.data, safe=False)

