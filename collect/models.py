import email
from django.db import models
from django.forms import DateField
from cloudinary.models import CloudinaryField
from django.db.models import Sum, Count
# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = CloudinaryField('image',default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location

    def save_events(self):
        self.save()
    
    @classmethod
    def new_events(cls):
        events = cls.objects.all()
        return events
        
class EventsAttendants(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

    def save_attendees(self):
        self.save()
class Post(models.Model):
    title = models.CharField(max_length=155)
    description = models.CharField(max_length=500, blank=True)
    photo = CloudinaryField('images', default='default.png')


    def __str__(self):
        return self.title
        
    def save_post(self):
        self.save()

    @classmethod
    def display_post(cls):
        posts = cls.objects.all()
        return posts

   
    @classmethod
    def search_by_title(cls,search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects
   

    def delete_post(self):
        self.delete()


class ReviewRating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
    
    def save_review(self):
        self.save()
        
    def averageReview(self):
        reviews = ReviewRating.objects.filter(post=self, status=True).aggregate(addition=Sum('rating'))
        sum = 0
        if reviews['addition'] is not None:
            sum = float(reviews['addition'])
        return sum

    def countReview(self):
        reviews = ReviewRating.objects.filter(post=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class Rating(models.Model):
    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    project = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    weight =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    content =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    usability =models.IntegerField(choices=RATE_CHOICES, default=0,blank=False)
    total = models.DecimalField(default=1, blank=False, decimal_places=2, max_digits=40)
    
    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return self.project.title
