from django.urls import path
from .views import CSVView, CSVDetailView

urlpatterns = [
   path('', CSVView.as_view()),
   path('<int:pk>/', CSVDetailView.as_view()),
]