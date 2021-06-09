from django.urls import path
from .views import DataView, DataDetailView, YearView ,YearAccountView, MonthView, MonthAccountView, MonthlyView, MonthlyAccountView

urlpatterns = [
   path('data', DataView.as_view(), name='data'),
   path('data/<int:pk>/', DataDetailView.as_view(), name='data_detail'),
   path('year', YearView.as_view(), name='year'),
   path('yearaccount', YearAccountView.as_view(), name='yearaccount'),
   path('month', MonthView.as_view(), name='month'),
   path('monthaccount', MonthAccountView.as_view(), name='monthaccount'),
   path('monthly', MonthlyView.as_view(), name='monthly'),
   path('monthlyaccount', MonthlyAccountView.as_view(), name='monthlyacccount'),
]