import keyword
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import random, string

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
  



class Category(TimeStampModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})  # Adjust 'category_detail' if your name is different
    
    def __str__(self):
        return self.name

    
class Tag(TimeStampModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    
class Blog(TimeStampModel):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default="UNKNOWN")
    content = models.TextField()
    read_time = models.IntegerField(null=True, blank=True)
    trend = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True,max_length=200, unique=True)
    image = models.URLField(null=True, blank=True)
    main_image = models.ImageField(upload_to='blog_image/',blank=True, null=True)
    author_image = models.URLField(default='https://png.pngtree.com/png-vector/20221110/ourmid/pngtree-silhouette-of-anonymous-man-in-mugshot-lineup-isolated-on-white-background-png-image_6441511.png')
    tag = models.ManyToManyField(Tag,null=True, blank=True)
    category = models.ManyToManyField(Category,related_name='blogs', null=True, blank=True)
    portfolio = models.BooleanField(default=False)
    keywords = models.TextField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        keywords_list = [
                "personal finance","financial tips","money management","saving money",
                "investing","debt reduction","passive income","retirement planning",
                "financial independence","compound interest","money-saving apps",
                "sustainable investing","credit score improvement","side hustles",
                "online shopping deals","cryptocurrency","financial security",
                "budgeting tips","financial literacy","smart money habits"
            ]
        
        for key in keywords_list :
            if not key in self.keywords :
                if not self.keywords.endswith(',') and self.keywords:
                    self.keywords += ', '
                self.keywords += key
        
        new_slug = False
        if not self.slug:
            new_slug = True
            self.slug = slugify(self.title)
        
        if not self.read_time:
            self.read_time = random.randint(10, 22)
        
        original_slug = self.slug
        if new_slug == True :
            while True :
                if Blog.objects.filter(slug=self.slug).exists() :
                    self.slug = f"{original_slug}-{random.randint(100000,9999999)}"
                else :
                    break
                
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
from adminsortable.models import SortableMixin

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('paragraph', 'Paragraph'),
        ('quote', 'Quote'),
        ('link', 'Link'),
        ('image', 'Image'),
        ('heading', 'Heading'),
        ('sub_heading', 'Sub_Heading'),
    ]
    blog = models.ForeignKey(Blog, related_name='contents', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    text_content = models.TextField(blank=True, null=True)
    image_url = models.ImageField(upload_to='blog_content/', null=True, blank=True)
    link_url = models.URLField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=200, default="UNKNOWN")
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.content_type} for {self.blog.title}"
    
    
    
  
  
class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # For nested comments

    def __str__(self):
        return f'Comment by {self.name} on {self.blog.title}'
    
    
class Task(models.Model):
    task_id = models.CharField(max_length=200, unique=True)
    description = models.TextField()

def generate_user_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=25))

class User(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='users')
    user_id = models.CharField(max_length=50, unique=True, default=generate_user_id)  # Use function here
    redirection_history = models.ManyToManyField('Blog', related_name='redirected_users')

    def has_visited_blog(self, blog):
        return self.redirection_history.filter(id=blog.id).exists()

    def __str__(self):
        return f"User {self.user_id} for Task {self.task.task_id}"
    
    
class MainRedirections(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="main_redirections")
    redirections_id = models.CharField(max_length=255, unique=True)
    final_link = models.URLField()

class RedirectBlogs(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='redirectblogs')
    configuration = models.ManyToManyField(Blog, related_name='redirectblogs_configuration')
    
class RandomRedirection(models.Model):
    genrated_redirections_id = models.CharField(max_length=25, unique=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    
    
class ContactDetails(models.Model):
    pass