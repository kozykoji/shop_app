from django.urls import path, include
from . import views
from shop_list.views import (
    IndexView, 
    PostDetailView, 
    TreatBrandsListView, 
    TreatBrandsPostView, 
    CommentFormView, 
    comment_approve,
    comment_remove,
    ReplyFormView,
    reply_approve,
    reply_remove,
)

urlpatterns = [
    path('home', views.home, name='home'),
    path('detail/<int:pk>', views.detail, name="detail"),
    path('addtoform/', views.addtoform, name='addtoform'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('treatblans/', TreatBrandsListView.as_view(), name='treatbrands_list'),
    path('treatbrands/<str:treatbrands_slug>/', TreatBrandsPostView.as_view(), name='treatbrands_post'),
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('comment/<int:pk>', CommentFormView.as_view(), name='comment_form'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
    path('reply/<int:pk>', ReplyFormView.as_view(), name='reply_form'),
    path('reply/<int:pk>/approve/', reply_approve, name='reply_approve'),
    path('reply/<int:pk>/remove/', reply_remove, name='reply_remove'),
    
    
]
