from django.shortcuts import render, redirect


def report_dashboard(request):

    return render(request, 'employees/view_report/index.html', {

    })
