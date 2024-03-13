from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from .models import Department, Position, Employee
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'employeeapp/home.html')

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
