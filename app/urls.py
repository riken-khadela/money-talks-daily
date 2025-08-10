from django.urls import path, include
from .views import (RedirectToHome, HomeView, TestView, BlogMainView, BlogDetailsView, TagViews, BlogSearchAPIView, CategoryDetailView, Contact, About, TermsAndConditions,MoreBlogsAPIView,
                    UploadBlogsAPIView, BlogDetailView, update_content_order)
from .portfolio_views import (MainPortfolioView, AboutPortfolioView, PortfolioGridView)
app_name = 'blog' 

urlpatterns = [
    path('', HomeView.as_view(), name='home-view'), 
    path('blogs/', BlogMainView.as_view(), name='blogs_main'), 
    path('contact/', Contact.as_view(), name='blogs_contact'), 
    path('about/', About.as_view(), name='blogs_about'), 
    path('TermsAndConditions/', TermsAndConditions.as_view(), name='blogs_TermsAndConditions'), 
    path('', RedirectToHome.as_view(), name='redirect-to-home'), 
    path('<slug:slug>/', BlogDetailsView.as_view(), name='blog_detail'),
    path('tags/<slug:slug>/', TagViews.as_view(), name='tag_view'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),  # Add this line

    path("api/search/", BlogSearchAPIView.as_view(), name="blog-search"),
    path("api/more-blogs/", MoreBlogsAPIView.as_view(), name="more-blogs"),
    path("api/more-portfolio/", MoreBlogsAPIView.as_view(), name="more-portfolio"),
    path("api/upload-blogs/", UploadBlogsAPIView.as_view(), name="upload-blogs"),
    
    # portfolio
    path('test/', TestView.as_view(), name='test'), 
    path('portfolio/', PortfolioGridView.as_view(), name='PortfolioGridView'), 
    path('portfolio/main/', MainPortfolioView.as_view(), name='portfolio'), 
    path('portfolio/about/', AboutPortfolioView.as_view(), name='Aboutportfolioview'), 
    
    path('admin/blog/<int:pk>/', BlogDetailView.as_view(), name='admin_blog_detail'),
    path('admin/app/update_order/', update_content_order, name='update_order'),


]
