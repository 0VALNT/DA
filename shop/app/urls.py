from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from django.contrib.staticfiles.views import serve
from .api import MessageModelViewSet, UserModelViewSet
from .views import *
from django.contrib.auth.views import *

def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)
router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    path('accounts/change_info/', change_info, name='change_info'),
    path('accounts/signup/', signup_view, name='signup'),
    path('accounts/update/', PasswordChangeView.as_view(template_name='registration/log.html'), name='update'),
    path('accounts/update/done', PasswordChangeDoneView.as_view(template_name='done.html'),
         name='password_change_done'),
    path('accounts/login/', LoginView.as_view(template_name='registration/log.html'), name='login'),
    path('accounts/logout/', log_out, name='logout'),
    path('accounts/profile/', profile_view, name='profile'),
    path('accounts/profile/<int:id>', delete_product_from_order, name='delete_product_from_order'),

    path('home/buy/<int:product_id>', buy_product, name='buy'),
    path('home/<int:product_id>', info_product, name='info_product'),
    path('home/delete/<int:id>', delete_product, name='delete_product'),
    path('home/', home_view, name='home'),
    path('', redirect_to_home, name='redirect_to_home'),
    path('home/feedback/', feedback_views, name='feedback'),

    path('admin_panel/', site_admin, name='admin'),
    path('admin_panel/analitic/<int:id>', analitic, name='analitic'),
    path('admin_panel/analitic/', analitic_list, name='analitic_list'),
    path('admin_panel/feedback_answer/<int:id>', feedback_answer, name='feedback_answer'),
    path('admin_panel/statistics', statistics, name='statistics'),
    path('admin_panel/statistics/details', detail_statistics, name='detail_statistics'),
    path('admin_panel/feedback_list/', feedback_list, name='feedback_list'),
    path('admin_panel/feedback_list/<int:id>', feedback_completed, name='feedback_completed'),
    path('admin_panel/<int:id>', complete_order, name='complete_order'),
    path('admin_panel/create_type', create_type, name='create_type'),
    path('admin_panel/create_product', create_product, name='create_product'),
    path('admin_panel/change_product/<int:id>', change_product, name='change_product'),

    path("password-reset", PasswordResetView.as_view(template_name="profile/password_reset.html"),
         name="password_reset"),
    path("password-reset/done/",
         PasswordResetDoneView.as_view(template_name="profile/password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>",
         PasswordResetConfirmView.as_view(template_name="profile/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path("password-reset-complete/",
         PasswordResetCompleteView.as_view(template_name="profile/reset_complete.html"),
         name="password_reset_complete"),

    path(r'api/v1/', include(router.urls)),

    re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
]
