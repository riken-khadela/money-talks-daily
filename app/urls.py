from django.urls import path, include
from .views import RedirectToHome, HomeView, TestView, BlogMainView, BlogDetailsView, TagViews, BlogSearchAPIView, CategoryDetailView, Contact, About, TermsAndConditions

app_name = 'blog' 

urlpatterns = [
    path('home/', HomeView.as_view(), name='home-view'), 
    path('test/', TestView.as_view(), name='test'), 
    path('blogs/', BlogMainView.as_view(), name='blogs_main'), 
    path('contact/', Contact.as_view(), name='blogs_contact'), 
    path('about/', About.as_view(), name='blogs_about'), 
    path('TermsAndConditions/', TermsAndConditions.as_view(), name='blogs_TermsAndConditions'), 
    path('', RedirectToHome.as_view(), name='redirect-to-home'), 
    path('blogs/<slug:slug>/', BlogDetailsView.as_view(), name='blog_detail'),
    path('tags/<slug:slug>/', TagViews.as_view(), name='tag_view'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),  # Add this line

    path("api/search/", BlogSearchAPIView.as_view(), name="blog-search"),
]
