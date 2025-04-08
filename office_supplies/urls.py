from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    UserSignUpView, UserLoginView, UserLogoutView,
    OfficeSupplyList, OfficeSupplyCreate, OfficeSupplyUpdate, 
    OfficeSupplyDelete, OfficeSupplyDetail,
    OfficeCategoryList, OfficeCategoryCreate, OfficeCategoryUpdate, 
    OfficeCategoryDelete, OfficeMassOutgoingCreateView,
    ExpiredItemListView, ExpiredItemDeleteView,
    OfficeReportView, LowStockListView, ExpiringSoonListView,
    OfficeReportsView, TransactionHistoryView
)
from django.contrib.auth import views as auth_views
from . import views

app_name = 'office_supplies'

urlpatterns = [
    # Authentication URLs
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # Supplies
    path('', OfficeSupplyList.as_view(), name='supply-list'),
    path('supplies/', OfficeSupplyList.as_view(), name='supply-list'),
    path('supplies/create/', OfficeSupplyCreate.as_view(), name='supply-create'),
    path('supplies/<int:pk>/', OfficeSupplyDetail.as_view(), name='supply-detail'),
    path('supplies/<int:pk>/update/', OfficeSupplyUpdate.as_view(), name='supply-update'),
    path('supplies/<int:pk>/delete/', OfficeSupplyDelete.as_view(), name='supply-delete'),
    
    # Operations
    path('operations/outgoing/', OfficeMassOutgoingCreateView.as_view(), name='mass-outgoing'),
    
    # Categories
    path('categories/', login_required(views.OfficeCategoryList.as_view()), name='category-list'),
    path('categories/new/', login_required(views.OfficeCategoryCreate.as_view()), name='category-create'),
    path('categories/<int:pk>/edit/', login_required(views.OfficeCategoryUpdate.as_view()), name='category-update'),
    path('categories/<int:pk>/delete/', login_required(views.OfficeCategoryDelete.as_view()), name='category-delete'),
    
    # Reports
    path('reports/', login_required(views.OfficeReportView.as_view()), name='reports'),
    path('low-stock/', LowStockListView.as_view(), name='low-stock'),
    path('expiring-soon/', ExpiringSoonListView.as_view(), name='expiring-soon'),
    
    # Expired Items
    path('expired/', ExpiredItemListView.as_view(), name='expired-list'),
    path('expired/<int:pk>/delete/', ExpiredItemDeleteView.as_view(), name='expired-delete'),
    
    # Bulk Import
    path('bulk-import/', views.bulk_import_view, name='bulk-import'),
    path('bulk-import/template/', views.download_template, name='download-template'),
    
    # Transactions
    path('transaction-history/', TransactionHistoryView.as_view(), name='transaction_history'),
    path('transaction-history/export/', views.export_transactions, name='export_transactions'),
    path('adjust/', views.adjust_inventory, name='adjust-inventory'),
    
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='office-password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='office-password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='office-password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='office-password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)