from django.shortcuts import render, redirect

from base_app.models import Regulations
from base_app.forms import RegulationsForm


def index_page(request):
    regulations = Regulations.objects.get(pk=1)

    return render(request, 'employees/manage_regulations/index.html', {
        'regulations': regulations,
    })


def edit_regulations(request):
    regulations = Regulations.objects.get(pk=1)
    form = RegulationsForm(request.POST or None, instance=regulations)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('manage_regulations_home')

    return render(request, 'employees/manage_regulations/edit_regulations.html', {
        'form': form,
    })
