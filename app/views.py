from django.shortcuts import render, redirect
from .models import FuelLitre, LitresBeforeNextTopUp, Sale, Price, Expense

from django.db.models import Q, Sum

from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from .forms import SaleForm, FuelLitreForm

from django.contrib import messages

from django.forms import modelformset_factory


@login_required
def home(request):
    if request.method == "POST":
        form = SaleForm(request.POST)

        form_one = FuelLitreForm(request.POST)

        if form_one.is_valid():
            # New reading on litres
            tank_litres = form_one.cleaned_data.get('fuel_litres')

            # Tank litres aftre top up and before next top up
            LitresBeforeNextTopUp.objects.create(litres=tank_litres)

            # Saving the new reading of litres in the tank after top up
            form_one.save()

            return redirect('home')

        if form.is_valid():
            # Creating an object but not saving it, this allows modification of objects's attribute value
            form_data = form.save(commit=False)
            
            # Form data submitted from the form
            current_fuel_reading = form.cleaned_data.get('total_sold_litres')

            # Fuel sales 
            total_litres = Sale.objects.all().order_by('-date')

            # Current price per fuel litre
            fuel_litre_price = Price.objects.all().order_by('-date')

            # Fuel litres in the tank before today's sold fuel litres
            previous_reading = LitresBeforeNextTopUp.objects.all().order_by('-date').first()

            if fuel_litre_price:
                # Current price per fuel litre
                price = fuel_litre_price.first()

                if not total_litres:
                    form_data.litres_per_day = current_fuel_reading
                    form_data.price_per_litre = price.price_per_litre
                    form_data.person = request.user

                    # Current fuel litres in the tank
                    current_litres = previous_reading.litres - current_fuel_reading

                    # Creating and saving an object of the current fuel reading 
                    LitresBeforeNextTopUp.objects.create(litres=current_litres)

                    # Saving the object to the database
                    form_data.save()

                    return redirect('home')

                

                latest_fuel_reading_object = total_litres.first()

                latest_fuel_reading = latest_fuel_reading_object.total_sold_litres

                # Finding litres per day by subtracting the previous day reading from the current day reading

                litres_per_day = current_fuel_reading - latest_fuel_reading

                form_data.litres_per_day = litres_per_day

                form_data.price_per_litre = price.price_per_litre

                form_data.person = request.user


                # Current fuel litres in the tank
                current_litres = previous_reading.litres - litres_per_day

                # Creating and saving an object of the current fuel reading in the tank
                LitresBeforeNextTopUp.objects.create(litres=current_litres)

                # Saving the form
                form_data.save()

                return redirect('home')
            

            messages.error(request, "Price per litre not set.")
            return redirect('home')


    
    
    form = SaleForm()
    form_one = FuelLitreForm()

    # FuelLitre model class latest instance
    initial_ltrs = FuelLitre.objects.all().order_by('-date')


    if initial_ltrs:
        initial_ltr = initial_ltrs.first()


        # Remaining fuel litres updates
        daily_fuel_updates = LitresBeforeNextTopUp.objects.filter(Q(date__date__gte=initial_ltr.date)).order_by('-date')

        # Paginating daily fuel litres update
        # daily_fuel_paginator = Paginator(daily_fuel_updates, 5)

        # page_num = request.GET.get('page')

        # daily_page_obj = daily_fuel_paginator.get_page(page_num)



        # Sales
        sales = Sale.objects.filter(Q(date__date__gte=initial_ltr.date)).order_by('-date')

        if sales:

            sales_list = []

            # Looping over the elements/instances/objects of the sales queryset
            for sale in sales:
                sale_dict = {}

                # sale object "litres_per_day" attribute value
                val_1 = sale.litres_per_day

                # sale object "price_per_litre" attribute value
                val_2 = sale.price_per_litre

                # Today total sold fuel amount
                total_sold_amount = round(val_1 * val_2, 2)

                # Adding an item to the dictionary object
                sale_dict[total_sold_amount] = sale

                # Posting/adding/appending the newly dictionary object to the list object

                sales_list.append(sale_dict)



            # Paginating the sales
            sales_paginator = Paginator(sales_list, 7)

            page_number = request.GET.get('pg')

            sales_page_obj = sales_paginator.get_page(page_number)



            # Total sold fuel litres so far
            sold_fuel_litres = Sale.objects.filter(Q(date__date__gte=initial_ltr.date)).aggregate(t_litres=Sum('litres_per_day'))

            # Price per litre
            litre_price = Price.objects.all().order_by('-date').first()

            # Total amount for consumed/sold fuel litres
            amount = round(sold_fuel_litres['t_litres'] * litre_price.price_per_litre, 2)

            # Fuel litres remaining in the tank
            remaining_fuel = round(initial_ltr.fuel_litres - sold_fuel_litres['t_litres'], 2)


            # consumed fuel litres rounded to 2 decimal places
            sold_fuel_ltrs = round(sold_fuel_litres['t_litres'], 2)


            # Litres of fuel sold since last top up
            consumed_fuel_litres = Sale.objects.filter(Q(date__date__gte=initial_ltr.date))

            # Total cost of consumed fuel litres
            consumed_fuel_amount = 0

            for obj in consumed_fuel_litres:
                consumed_fuel_amount += (obj.litres_per_day * obj.price_per_litre)




            context = {'sales_page_obj': sales_page_obj, 'daily_page_obj': daily_fuel_updates,
                   'sales': sales_list, 'form': form, 'formm': form_one, 'initial_litres_object': initial_ltr,
                   'fuel_sold_litres': sold_fuel_ltrs, 'amount': amount, 'remainder': remaining_fuel, 
                   'total': round(consumed_fuel_amount, 2)}
               
            return render(request, "app/home.html", context)

        context = {'form': form, 'formm': form_one, 'initial_litres_object': initial_ltr}
        return render(request, "app/home.html", context)

    context = {'form': form, 'formm': form_one}
    return render(request, "app/home.html", context)


# View to add expenses of the day
@login_required 
def expenses(request):
    ExpenseForm = modelformset_factory(Expense, fields=['expense_name', 'expense_amount'], can_delete=True, extra=2)
    if request.method == "POST":
        
        formset = ExpenseForm(request.POST)

        if formset.is_valid():
                
            form_objects = formset.save(commit=False)

            for form_object in form_objects:
                form_object.user = request.user
                form_object.save()

            for obj in formset.deleted_objects:
                obj.delete()

            messages.success(request, "Data captured successfully")
            return redirect('expenses')

    
    # Queryset for none return objects
    queryset = Expense.objects.none()
    
    # Instatiating the formset class
    formset = ExpenseForm(queryset=queryset)

    # FuelLitre model class latest instance
    initial_ltrs = FuelLitre.objects.all().order_by('-date')


    if initial_ltrs:
        initial_ltr = initial_ltrs.first()
        
        # Expenses base on a particular latest instance of "FuelLitre" model class
        expenses_incurred = Expense.objects.filter(Q(date__gte=initial_ltr.date)).order_by('-date')

        # An empty set to hold unique dates for expenses got incurred
        unique_date = set()
        
        # Looping over the expenses objects, filtering the value of the date attribute
        for expense in expenses_incurred:
            unique_date.add(expense.date)
        
        # Dictionary object to capture date as a key and expenses incurred on that particular date as a value to the key
        expenses_dict = {}

        # Looping over the set object "unique_date"
        for u_date in unique_date:
            date_expenses = Expense.objects.filter(Q(date=u_date))

            expenses_dict[u_date] = date_expenses

        
        # Total expenses as from a specified date
        expenses_amt = Expense.objects.filter(Q(date__gte=initial_ltr.date)).aggregate(t_expense=Sum('expense_amount'))

        
        context = {'expenses': expenses_dict, 'total': expenses_amt, 'formset': formset}
        return render(request, "app/expenses.html", context)
        
    context = {'formset': formset}
    return render(request, "app/expenses.html", context)



