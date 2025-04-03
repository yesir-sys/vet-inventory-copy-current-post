from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import MassOutgoing

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

class MassOutgoingListView(ListView):
    model = MassOutgoing
    template_name = 'inventory/mass_outgoing_list.html'  # Changed from vet_supplies to inventory
    context_object_name = 'mass_outgoings'
    paginate_by = 10