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

# Create your views here.


class HomeView(TemplateView):
    
    template_name = "pages/index.html"
    def get(self, request):
        blogs = Blog.objects.filter(trend=False)
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            if len(blog.content) > 75 :
                blog.content = blog.content[:75] + '...'
                
        trending_blogs = Blog.objects.filter(trend=True)
        for trending_blog in trending_blogs:
            trending_blog.full_url = request.build_absolute_uri(trending_blog.get_absolute_url())
            if len(trending_blog.content) > 75 :
                trending_blog.content = trending_blog.content[:140] + '...'
                
        return render(request, self.template_name, {'blogs': blogs,"trending_blogs" : trending_blogs})
    
    
    
class TestView(TemplateView):
    
    template_name = "pages/test.html"
    def get(self, request):
        
        return render(request, self.template_name)
    
    def post(self,request):
        return render(request,self.template_name)
    
class Contact(TemplateView):
    
    template_name = "pages/contact.html"
    def get(self, request):
        
        return render(request, self.template_name)
    
    def post(self,request):
        return render(request,self.template_name)
    
class RedirectToHome(TemplateView):
    
    def get(self, request):
        return redirect('/home/')
    
    
    
class BlogMainView(TemplateView):
    
    template_name = "pages/blog_main_page.html"
    def get(self, request):
        blogs = Blog.objects.filter(trend=False)
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            if len(blog.content) > 75 :
                blog.content = blog.content[:75] + '...'
                
        trending_blogs = Blog.objects.filter(trend=True)
        for trending_blog in trending_blogs:
            trending_blog.full_url = request.build_absolute_uri(trending_blog.get_absolute_url())
            if len(trending_blog.content) > 75 :
                trending_blog.content = trending_blog.content[:140] + '...'
        
        # categories = Category.objects.annotate(blog_count=Count('blogs')).order_by('-blog_count')[:7]
        # for trending_cat in categories:
        #     trending_cat.full_url = request.build_absolute_uri(trending_cat.get_absolute_url())
                
        return render(request, self.template_name, {'blogs': blogs,"trending_blogs" : trending_blogs})
    
    def post(self,request):
        return render(request,self.template_name)
    
    
from .models import (Blog, User, MainRedirections, Task
                     , RedirectBlogs, RandomRedirection
                     )

class BlogDetailsView(TemplateView):
    
    template_name = "pages/blog_details_page.html"
    
    def get_redirect_blog_link(self, task_id, user):
        """ Get the next blog for redirection. """
        if not task_id:
            return None

        # Fetch the task
        task = Task.objects.filter(task_id=task_id).first()
        if not task:
            return None

        # If the user has visited all the blogs, return None
        visited_blogs = user.redirection_history.all()
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

        # Get or create a user associated with the task
        if user_id:
            user = User.objects.filter(user_id=user_id, task__task_id=task_id).first()
        else:
            # If no user_id, create a new anonymous user for the task
            user = User.objects.create(task=Task.objects.get(task_id=task_id))

        # Add current blog to the user's redirection history
        blog = get_object_or_404(Blog, slug=slug)
        user.redirection_history.add(blog)

        # Check for the next blog to redirect to
        next_blog = self.get_redirect_blog_link(task_id, user)

        # If there's a next blog, pass it to the context
        next_blog_url = None
        if next_blog:
            next_blog_url = next_blog.get_absolute_url() + f"?task_id={task_id}&user_id={user.user_id}"

        # Determine if this is the last blog in the task sequence
        task = Task.objects.filter(task_id=task_id).first()
        is_last_blog = not next_blog  # If there is no next blog, it's the last blog

        # Render the current blog with the next blog URL
        return self.render_blog_detail(request, blog, next_blog_url, task, is_last_blog)
    
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
        
        return render(request, self.template_name, {
            'blogs': blog,
            "contents": Content.objects.filter(blog=blog).order_by('created_at'),
            "related_blogs": related_blogs,
            'comments': comments,
            "tags": blog.tag.all(),
            "post_categories": post_categories,
            "recent_blogs": recent_blogs,
            "next_blog_url": next_blog_url,  # Include the next blog URL if it exists
            "task": task,  # Pass the task content if it exists
            "is_last_blog": is_last_blog,
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
    
    
class SearchView(View):
    def get(self, request):
        breakpoint()
        query = request.GET.get('q')
        results = []
        if query:
            results = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).values('id', 'title', 'content', 'slug')
        
        return JsonResponse({'results': list(results)}) 


    
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
        
        

def custom_404(request, exception):
    """Custom 404 error page"""
    return render(request, 'pages/404.html', status=404)