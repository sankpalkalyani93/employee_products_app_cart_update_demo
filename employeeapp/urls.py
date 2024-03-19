from django.urls import path
from . import views
from .views import EmployeeListView, PositionListView, DepartmentListView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('main/', views.main_template, name='main_template'),
    path('search/', views.search_results, name='search_results'),
    path('employee_detail_view/<int:employee_id>/', views.employee_detail_view, name='employee_detail_view'),
    path('employee_list_view/', EmployeeListView.as_view(), name='employee_list_view'),
    path('position_list_view/', PositionListView.as_view(), name='position_list_view'),
    path('department_list_view/', DepartmentListView.as_view(), name='department_list_view'),  
    path('create_product/', views.create_product, name='create_product'),
    path('products_list/', views.products_list, name='products_list'),
    path('product_detail_view/<int:id>', views.product_detail_view, name='product_detail_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]