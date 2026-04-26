from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/appointments/', include('appointments.urls')),
    path('api/edr/', include('edr.urls')),
    path('api/pharmacy/', include('pharmacy.urls')),
    path('api/billing/', include('billing.urls')),
    path('api/communication/', include('communication.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/staff/', include('staff.urls')),
    path('api/analytics/', include('analytics.urls')),
]
