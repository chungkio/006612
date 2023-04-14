from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = (
    path('', views.ViewDiscountCode.as_view()),
    path('detail/<int:pk>', views.ViewDetailDiscountCode.as_view()),
    path('create', views.CreatePostDiscountCode.as_view()),
    path('detail/<int:pk>/update', views.UpdatePostDiscountCode.as_view()),
    path('delete', views.DeletePostDiscountCode.as_view()),
    path('user/list', views.GetUserDiscountStatus.as_view()),
    path('user/<int:user_id>/status', views.UserIdDiscountStatus.as_view(), name='get_user_id_discount_status'),
    path('user/filter-by-status', views.FilterUserDiscountByStatus.as_view(), name='filtered_user_discount_status'),
)