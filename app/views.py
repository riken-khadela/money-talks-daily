from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView

import blog
from .models import (Blog, Content,
                     Comment, Tag, Category,
                     RandomRedirection ,
                     RedirectBlogs ,
                     MainRedirections
                     )
from django.db.models import Count
import random, string
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


class HomeView(TemplateView):
    
    template_name = "pages/index.html"
    
    def get(self, request):
        
        path = [
            "Home"
        ]
        # Retrieve search query from request
        search_query = request.GET.get('search', '').strip()

        # Fetch the trending blog
        trending_blog = Blog.objects.filter(trend=True).order_by('?').first()
        if trending_blog:
            trending_blog.full_url = request.build_absolute_uri(trending_blog.get_absolute_url())
            trending_blog.content = trending_blog.content[:140] + '...' if len(trending_blog.content) > 140 else trending_blog.content

        # Fetch blogs based on the search query or exclude the trending blog
        if search_query:
            blogs = Blog.objects.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(author__icontains=search_query)
            ).distinct()
        else:
            blogs = Blog.objects.exclude(id=trending_blog.id if trending_blog else None)

        # Annotate blogs with full URLs and truncated content
        
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            blog.content = blog.content[:75] + '...' if len(blog.content) > 75 else blog.content

        # Context for rendering the template
        
        for blg in blogs : blg.content
        context = {
            'blogs': blogs,
            "trending_blogs": [trending_blog] if trending_blog else [],
            'path' : path
        }

        return render(request, self.template_name, context)
    
    
class TestView(TemplateView):
    
    template_name = "portfolio/index.html"
    def get(self, request):
        
        return render(request, self.template_name)
    
    def post(self,request):
        return render(request,self.template_name)
    
class Contact(TemplateView):
    
    template_name = "pages/contact.html"
    def get(self, request):
        path = [
            "Home",
            "Contacts",
        ]
        
        
        return render(request, self.template_name,{'path' : path})
    
    def post(self,request):
        return render(request,self.template_name)
    
class About(TemplateView):
    
    template_name = "pages/about.html"
    def get(self, request):
        path = [
            "Home",
            "About",
        ]
        return render(request, self.template_name,{'path' : path})
    
    def post(self,request):
        return render(request,self.template_name)
    
class TermsAndConditions(TemplateView):
    
    template_name = "pages/TermsAndConditions.html"
    def get(self, request):
        
        path = [
            "Home",
            "TermsAndConditions",
        ]
        return render(request, self.template_name,{'path' : path})
        
    def post(self,request):
        return render(request,self.template_name)
    
class RedirectToHome(TemplateView):
    
    def get(self, request):
        return redirect('/home/')
    
    
    
class BlogMainView(TemplateView):
    
    template_name = "pages/blog_main_page.html"
    def get(self, request):
        path = [
            "Home",
            "Blogs",
        ]
        blogs = Blog.objects.filter(portfolio=False).order_by('?')
        if len(blogs) >= 8 :
            blogs = blogs[:8]
            
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            if len(blog.content) > 75 :
                blog.content = blog.content[:75] + '...'
        return render(request, self.template_name, {'blogs': blogs, 'path' : path})
    
    def post(self,request):
        return render(request,self.template_name)
    
    
from .models import (Blog, User, MainRedirections, Task
                     , RedirectBlogs, RandomRedirection
                     )
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class BlogDetailsView(TemplateView):
    
    template_name = "pages/blog_details_page.html"
    
    def get_redirect_blog_link(self, task_id, user):
        """ Get the next blog for redirection (limit to 3 redirects). """
        if not task_id:
            return None

        # Fetch the task
        task = Task.objects.filter(task_id=task_id).first()
        if not task:
            return None

        # If the user has already visited 3 blogs, stop redirection
        visited_blogs = user.redirection_history.all()
        if visited_blogs.count() >= 4:
            return None  # Stop redirection

        # Get remaining blogs excluding already visited ones
        remaining_blogs = Blog.objects.exclude(id__in=visited_blogs.values('id')).order_by('?')

        if remaining_blogs.exists():
            # Get the next random blog that the user hasn't visited
            next_blog = remaining_blogs.first()
            return next_blog
        return None

    def get(self, request, slug):
        """ Handles redirection and rendering of the blog details. """
        task_id = request.GET.get('task_id', None)
        user_id = request.GET.get('user_id', None)

        # If no task_id, just show the normal blog
        if not task_id:
            blog = get_object_or_404(Blog, slug=slug)
            return self.render_blog_detail(request, blog, None)

        # Get the task (if exists)
        task_obj = Task.objects.filter(task_id=task_id).first()
        if not task_obj:
            blog = get_object_or_404(Blog, slug=slug)
            return self.render_blog_detail(request, blog, None)

        # Get or create a user associated with the task
        if user_id:
            user = User.objects.filter(user_id=user_id, task__task_id=task_id).first()
        else:
            # If no user_id, create a new anonymous user for the task
            user = User.objects.create(task=task_obj)

        # Add current blog to user's redirection history
        blog = get_object_or_404(Blog, slug=slug)
        user.redirection_history.add(blog)

        # Check if the user has already visited 3 blogs
        if user.redirection_history.count() >= 3:
            next_blog_url = None  # Stop further redirection
            is_last_blog = True
        else:
            # Get the next blog for redirection
            next_blog = self.get_redirect_blog_link(task_id, user)
            next_blog_url = next_blog.get_absolute_url() + f"?task_id={task_id}&user_id={user.user_id}" if next_blog else None
            is_last_blog = next_blog is None

        # Render the blog with next blog link
        return self.render_blog_detail(request, blog, next_blog_url, task_obj, is_last_blog)
    
    def render_blog_detail(self, request, blog, next_blog_url, task=None, is_last_blog=False):
        """ Helper method to render blog details. """
        related_blogs = Blog.objects.filter(tag__in=blog.tag.all()).exclude(id=blog.id).distinct()[:3]
        for related_blg in related_blogs:
            related_blg.full_url = request.build_absolute_uri(related_blg.get_absolute_url())
            if len(related_blg.content) > 75:
                related_blg.content = related_blg.content[:140] + '...'

        comments = blog.comments.all()
        post_categories = Tag.objects.annotate(blog_count=Count('blog')).order_by('-blog_count')[:8]
        for post_categorie in post_categories:
            post_categorie.full_url = request.build_absolute_uri().split('blogs/')[0] + "tags/" + post_categorie.slug + "/"
        post_categories = list(post_categories)
        random.shuffle(post_categories)

        recent_blogs = Blog.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:5]

        # Render template with context
        path = [
            "Home",
            "Blogs",
            blog.title
        ]
        data = {
            'blogs': blog,
            "contents": Content.objects.filter(blog=blog).order_by('order'),
            "related_blogs": related_blogs,
            'comments': comments,
            "tags": blog.tag.all(),
            "post_categories": post_categories,
            "recent_blogs": recent_blogs,
            "next_blog_url": next_blog_url,  # Include the next blog URL if it exists
            "task": task,  # Pass the task content if it exists
            "is_last_blog": is_last_blog,
            "path" : path
        }
        print(data)
        return render(request, self.template_name, {
            'blogs': blog,
            "contents": Content.objects.filter(blog=blog).order_by('order'),
            "related_blogs": related_blogs,
            'comments': comments,
            "tags": blog.tag.all(),
            "post_categories": post_categories,
            "recent_blogs": recent_blogs,
            "next_blog_url": next_blog_url,  # Include the next blog URL if it exists
            "task": task,  # Pass the task content if it exists
            "is_last_blog": is_last_blog,
            "path" : path
        })
        
        
    def post(self, request, slug):
        """ Handles comment submission for a blog. """
        blog = get_object_or_404(Blog, slug=slug)

        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)
        else:
            parent_comment = None

        new_comment = Comment(
            blog=blog,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            website=request.POST.get('web'),
            content=request.POST.get('comment'),
            parent=parent_comment  # Set the parent for replies
        )
        new_comment.save()

        return redirect(blog.get_absolute_url())
    
class TagViews(TemplateView):
    
    template_name = "pages/tag_main_page.html"
    def get(self, request, slug):
        # Fetch the tag based on the slug
        tag = get_object_or_404(Tag, slug=slug)
        
        # Retrieve all blogs associated with the tag
        blogs = Blog.objects.filter(tag=tag).distinct()
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            if len(blog.content) > 75:
                blog.content = blog.content[:75] + '...'

        # Fetch trending blogs
        trending_blogs = Blog.objects.filter(trend=True)
        for trending_blog in trending_blogs:
            trending_blog.full_url = request.build_absolute_uri(trending_blog.get_absolute_url())
            if len(trending_blog.content) > 75:
                trending_blog.content = trending_blog.content[:140] + '...'

        # Fetch the most popular tags
        popular_tags = Tag.objects.annotate(blog_count=Count('blog')).order_by('-blog_count')[:12]
        for tag_item in popular_tags:
            tag_item.full_url = request.build_absolute_uri().split('tags/')[0] + "tags/" + tag_item.slug + "/"

        return render(request, self.template_name, {
            'tag': tag,
            'blogs': blogs,
            'trending_blogs': trending_blogs,
            'popular_tags': popular_tags,
        })

    
    def post(self,request):
        return render(request,self.template_name)
    
    
class BlogSearchAPIView(View):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response({"error": "Query parameter `q` is required."}, status=400)

        # Perform the search
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |  
            Q(content__icontains=query) |  
            Q(author__icontains=query)  
        ).distinct()

        results = [
            {
                "title": blog.title,
                "author": blog.author,
                "url": blog.get_absolute_url(),
                "excerpt": blog.content[:140] + "..." if len(blog.content) > 140 else blog.content,
                "image": blog.image,
            }
            for blog in blogs
        ]

        return Response({"results": results}, status=200)
    
from rest_framework.views import APIView
import json
@method_decorator(csrf_exempt, name='dispatch')
class MoreBlogsAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON body
            body = json.loads(request.body)
            exclude_ids = body.get('id', [])
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

        # Validate that exclude_ids is a list
        if not isinstance(exclude_ids, list):
            return JsonResponse({"error": "'ids' must be a list."}, status=400)

        # Fetch blogs excluding given IDs
        blogs = Blog.objects.filter(portfolio=False).exclude(id__in=exclude_ids).order_by('-created_at')[:8]

        # Serialize blog data
        results = [
            {
                "id": blog.id,
                "title": blog.title,
                "author": blog.author,
                "url": blog.get_absolute_url(),
                "excerpt": blog.content[:75] + '...' if len(blog.content) > 75 else blog.content,
                "image": blog.main_image.url,
                "created_at": blog.created_at.strftime('%b %d, %Y'),
            }
            for blog in blogs
        ]

        return JsonResponse({"results": results}, status=200)


    
class CategoryDetailView(TemplateView):
    template_name = "pages/category_detail.html"

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug) 
        blogs = category.blogs.all()
        if len(blogs) >= 12 :
            blogs = blogs[:12]
        
        
        return render(request, self.template_name, {
            'category': category,
            'blogs': blogs,
        })
        
        

    
@method_decorator(csrf_exempt, name='dispatch')
class UploadBlogsAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            
            body = json.loads(request.body)
            exclude_ids = body.get('id', [])
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

        # Validate that exclude_ids is a list
        if not isinstance(exclude_ids, list):
            return JsonResponse({"error": "'ids' must be a list."}, status=400)

        # Fetch blogs excluding given IDs
        blogs = Blog.objects.filter(portfolio=False).exclude(id__in=exclude_ids).order_by('-created_at')[:8]

        # Serialize blog data
        results = [
            {
                "id": blog.id,
                "title": blog.title,
                "author": blog.author,
                "url": blog.get_absolute_url(),
                "excerpt": blog.content[:75] + '...' if len(blog.content) > 75 else blog.content,
                "image": blog.main_image.url,
                "created_at": blog.created_at.strftime('%b %d, %Y'),
            }
            for blog in blogs
        ]

        return JsonResponse({"results": results}, status=200)

        

def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'pages/404.html', status=404)


[
    {
        ""
    }
]

from django.views.generic.detail import DetailView

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'admin/blog_detail.html'
    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Content

@csrf_exempt
def update_content_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                content = Content.objects.get(id=item['id'])
                content.order = item['order']
                content.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
