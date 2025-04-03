from django import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import (
    CategoryDelete, UserSignUpView, UserLoginView, UserLogoutView,
    VetSupplyList, VetSupplyCreate, VetSupplyUpdate, 
    VetSupplyDelete, VetSupplyDetail,
    VetCategoryList, VetCategoryCreate, VetCategoryUpdate, VetCategoryDelete,
    ExpiredItemListView, ExpiredItemDeleteView,
    MassAddView, DownloadCSVTemplateView, MassOutgoingCreateView,
    VetReportView,
    LowStockListView, ExpiringSoonListView, ReportsView,
    TransactionHistoryView,
)
from django.contrib.auth import views as auth_views

app_name = 'vet_supplies'  # Define the namespace

urlpatterns = [
    # Authentication URLs
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Supplies URLs
    path('', VetSupplyList.as_view(), name='supply-list'),
    path('create/', VetSupplyCreate.as_view(), name='supply-create'),
    path('detail/<int:pk>/', VetSupplyDetail.as_view(), name='supply-detail'),
    path('update/<int:pk>/', VetSupplyUpdate.as_view(), name='supply-update'),
    path('delete/<int:pk>/', VetSupplyDelete.as_view(), name='supply-delete'),

    # Operations URLs
    path('operations/outgoing/', login_required(MassOutgoingCreateView.as_view()), name='mass-outgoing'),

    # Categories URLs
    path('categories/', VetCategoryList.as_view(), name='category-list'),
    path('categories/create/', VetCategoryCreate.as_view(), name='category-create'),
    path('categories/update/<int:pk>/', VetCategoryUpdate.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', CategoryDelete.as_view(), name='category-delete'),

    # Reports URLs
    path('reports/', VetReportView.as_view(), name='vreports'),

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='vet-password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='vet-password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='vet-password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='vet-password_reset_complete'),
    
    # Monitoring URLs
    path('low-stock/', LowStockListView.as_view(), name='low-stock'),
    path('expiring-soon/', ExpiringSoonListView.as_view(), name='expiring-soon'),

    # Bulk Import URLs
    path('bulk-import/', views.bulk_import_view, name='bulk-import'),
    path('bulk-import/template/', views.download_template, name='download-template'),

    # Transaction History URLs
    path('transaction-history/', TransactionHistoryView.as_view(), name='transaction_history'),
    path('transaction-history/export/', views.export_transactions, name='export_transactions'),
    path('adjust/', views.adjust_inventory, name='adjust-inventory'),
]

# Static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
