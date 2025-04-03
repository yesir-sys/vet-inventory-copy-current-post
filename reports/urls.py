from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'reports'

urlpatterns = [
    path('', login_required(views.dashboard), name='dashboard'),
    path('export/', views.export_report, name='export'),
    path('<str:supply_type>/category/<str:category>/', login_required(views.view_by_category), name='view-category'),
    path('<str:supply_type>/low-stock/', login_required(views.view_low_stock), name='view-low-stock'),
    path('<str:supply_type>/movements/<str:movement_type>/', login_required(views.view_movements), name='view-movements'),
    path('view-low-stock/<str:supply_type>/', views.view_low_stock, name='view-low-stock'),
    path('view-movements/<str:supply_type>/<str:movement_type>/', views.view_movements, name='view-movements'),
]
