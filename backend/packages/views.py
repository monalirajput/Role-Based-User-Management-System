from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package
from .forms import PackageForm
from django.contrib import messages

# LIST
def package_list(request):
    packages = Package.objects.all()
    return render(request, 'packages/package_list.html', {'packages': packages})

# CREATE
def package_create(request):
    form = PackageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Package Added Successfully")
        return redirect('package_list')
    return render(request, 'packages/package_form.html', {'form': form})

# UPDATE
def package_update(request, pk):
    package = get_object_or_404(Package, pk=pk)
    form = PackageForm(request.POST or None, instance=package)
    if form.is_valid():
        form.save()
        messages.success(request, "Package Updated Successfully")
        return redirect('package_list')
    return render(request, 'packages/package_form.html', {'form': form})

# DELETE
def package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.delete()
    messages.success(request, "Package Deleted Successfully")
    return redirect('package_list')