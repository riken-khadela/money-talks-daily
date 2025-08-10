
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView

import json
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


class MainPortfolioView(TemplateView):
    
    template_name = "portfolio/index.html"
    def get(self, request):
        
        return render(request, self.template_name)
    
    def post(self,request):
        return render(request,self.template_name)

class PortfolioGridView(TemplateView):
    
    template_name = "portfolio/grid.html"
    def get(self, request):
        path = [
            "Home",
            "portfolios",
        ]
        blogs = Blog.objects.filter(portfolio=True).order_by('?')
        if len(blogs) >= 8 :
            blogs = blogs[:8]
            
        for blog in blogs:
            blog.full_url = request.build_absolute_uri(blog.get_absolute_url())
            if len(blog.content) > 75 :
                blog.content = blog.content[:75] + '...'
        return render(request, self.template_name, {'blogs': blogs, 'path' : path})
    
    def post(self,request):
        return render(request,self.template_name)


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
        blogs = Blog.objects.exclude(id__in=exclude_ids).order_by('-created_at')[:8]

        # Serialize blog data
        results = [
            {
                "id": blog.id,
                "title": blog.title,
                "author": blog.author,
                "url": blog.get_absolute_url(),
                "excerpt": blog.content[:75] + '...' if len(blog.content) > 75 else blog.content,
                "image": blog.main_image,
                "created_at": blog.created_at.strftime('%b %d, %Y'),
            }
            for blog in blogs
        ]

        return JsonResponse({"results": results}, status=200)



class AboutPortfolioView(TemplateView):
    
    template_name = "portfolio/aboutme.html"
    def get(self, request):
        path = [
            "portfolio",
            "About",
        ]
        return render(request, self.template_name,{'path' : path})
    
    def post(self,request):
        return render(request,self.template_name)