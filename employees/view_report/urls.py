from django.urls import path

from base_app.decorators import employee_only

from .views import *

urlpatterns = [
    path('', report_dashboard, name='report_dashboard'),
]


# restrict whole app to employees only
def dec_patterns(patterns):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = employee_only(callback)
        pattern._callback = employee_only(callback)
        decorated_patterns.append(pattern)
    return decorated_patterns


url_patterns = dec_patterns(urlpatterns)