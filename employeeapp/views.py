from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from employeeapp.forms import ProductsForm
from .models import Department, Position, Employee, Products
from django.db.models import Q
from PIL import Image
from io import BytesIO

# Create your views here.
def home(request):
    request.session['my_data'] = 'Hello, Session!'
    my_data = request.session.get('my_data', 'Default value if not found')
    username = request.session.get('username')
    return render(request, 'employeeapp/home.html', {'my_data': my_data, 'username': username})

def main_template(request):
    employees = Employee.objects.all()
    positions = Position.objects.all()
    departments = Department.objects.all()

    employee_list_view_url = reverse('employee_list_view')
    position_list_view_url = reverse('position_list_view')
    department_list_view_url = reverse('department_list_view')

    #return render(request, 'main_template.html', {'employees': employees, 'positions': positions, 'departments': departments}) 
    return render(request, 'main_template.html', {
        'employees': employees,
        'positions': positions,
        'departments': departments,
        'employee_list_view_url': employee_list_view_url,
        'position_list_view_url': position_list_view_url,
        'department_list_view_url': department_list_view_url,
    })

def search_results(request):
    #query = request.GET.get('q')
    #results = Employee.objects.filter(first_name__icontains=query)  # Assuming Employee is your model
    #return render(request, 'search_results.html', {'query': query, 'results': results})
    query = request.GET.get('q')

    employee_results = None
    department_results = None

    if query:
        employee_results = Employee.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(department__dname__icontains=query)
        ).distinct()

        department_results = Department.objects.filter(
            Q(dname__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {'employee_results': employee_results, 'department_results': department_results, 'query': query})

def employee_detail_view(request, employee_id):
    employees = Employee.objects.get(pk = employee_id)
    return render(request, 'employeeapp/employee_detail_view.html', {'employees': employees})

class DepartmentListView(ListView):
    model = Department
    template_name = 'employeeapp/department_list_view.html'
    context_object_name = 'departments'

class PositionListView(ListView):
    model = Position 
    template_name = 'employeeapp/position_list_view.html'
    context_object_name = 'positions'

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employeeapp/employee_list_view.html'
    context_object_name = 'employees'

def create_product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)  # Get the product instance without saving to the database yet

            # Resize the uploaded image before saving
            if product.image:
                img = Image.open(product.image)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.thumbnail((300, 300))
                
                # Save the resized image back to the product instance
                output_io = BytesIO()
                img.save(output_io, format='JPEG', quality=100)
                product.image.save(product.image.name, output_io)

            # Save the product instance to the database
            product.save()
            return redirect('products_list')
    else:
        form = ProductsForm()
    
    return render(request, 'employeeapp/create_product.html', {'form': form})
    
def products_list(request):
    products = Products.objects.all()
    return render(request, 'employeeapp/products_list.html', {'products': products})

def product_detail_view(request, id):
    product = Products.objects.get(id=id)
    return render(request, 'employeeapp/product_detail_view.html', {'product': product})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    #messages.info(request, 'Logout successful.')
    return render(request, 'logout.html')