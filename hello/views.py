from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import transaction
from .models import Apartment
from .forms import ApartmentForm
from django.urls import reverse



def apartment_create(request):
    if request.method == 'POST':
        with transaction.atomic():
            form = ApartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('apartment_list')
    else:
        form = ApartmentForm()

    return render(request, 'apartment_form.html', {'form': form})

def apartment_update(request, id):
    apartment = get_object_or_404(Apartment, id=id)

    if request.method == 'POST':
        with transaction.atomic():
            form = ApartmentForm(request.POST, instance=apartment)
            if form.is_valid():
                form.save()
                return redirect('apartment_list')
    else:
        form = ApartmentForm(instance=apartment)

    return render(request, 'apartment_form.html', {'form': form})

def apartment_delete(request, id):
    apartment = get_object_or_404(Apartment, id=id)

    if request.method == 'POST':
        with transaction.atomic():
            apartment.delete()
            return redirect('apartment_list')

    return render(request, 'apartment_confirm_delete.html', {'apartment': apartment})


def reserve_apartment(request, id):
    with transaction.atomic():
        apt = Apartment.objects.select_for_update().get(id=id)

        if apt.is_reserved:
            return HttpResponse(
                f'Already reserved<br><br><a href="{reverse("apartment_list")}">⬅ Back</a>'
            )

        apt.is_reserved = True
        apt.save()

        return HttpResponse(
            f'Reserved successfully<br><br><a href="{reverse("apartment_list")}">⬅ Back</a>'
        )

def apartment_list(request):
    apartments = Apartment.objects.all()

    # Get filter parameters
    company_name = request.GET.get('company_name')
    complex_name = request.GET.get('complex_name')
    location = request.GET.get('location')
    max_price = request.GET.get('max_price')
    min_price = request.GET.get('min_price')
    min_lease_length = request.GET.get('min_lease_length')
    max_lease_length = request.GET.get('max_lease_length')
    order = request.GET.get('order')

    # Apply filters when values exist
    if company_name:
        apartments = apartments.filter(company_name__icontains=company_name)
    if complex_name:
        apartments = apartments.filter(complex_name__icontains=complex_name)
    if location:
        apartments = apartments.filter(location__icontains=location)
    if max_price:
        apartments = apartments.filter(price__lte=max_price)
    if min_price:
        apartments = apartments.filter(price__gte=min_price)
    if min_lease_length:
        apartments = apartments.filter(lease_length__gte=min_lease_length)
    if max_lease_length:
        apartments = apartments.filter(lease_length__lte=max_lease_length)

    # Ordering conditions
    if order == "price_asc":
        apartments = apartments.order_by("price")
    elif order == "price_desc":
        apartments = apartments.order_by("-price")
    elif order == "newest":
        apartments = apartments.order_by("lease_start_date")
    elif order == "lease_asc":
        apartments = apartments.order_by("lease_length")
    elif order == "lease_desc":
        apartments = apartments.order_by("-lease_length")
    else:
        apartments = apartments.order_by("id")

    return render(request, 'apartment_list.html', {'apartments': apartments})


def home(request):
    return render(request, 'home.html')
