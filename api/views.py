# Rest Framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Django
from .models import DataModel
from .serializers import DataSerializer
from django.db.models import Sum
from django.db.models import Func
from django.db.models.functions import Substr

# Python
import time
    
class DataView(generics.ListCreateAPIView):
    queryset = DataModel.objects.all()
    serializer_class = DataSerializer

    def create(self, request, *args, **kwargs):
        # Check if the post contains just 1 item, then it is a dictionary
        if isinstance(request.data, dict):
            serializer = self.get_serializer(data=request.data)
        # Check if the post contains several items, then it is a list
        elif isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class DataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DataModel.objects.all()
    serializer_class = DataSerializer

class YearView(APIView):
    # List
    def get(self, request, format=None): 
        queryset = DataModel.objects.values('account').order_by('account').annotate(balance=Round(Sum('amount')))
        output = {'data': queryset}
        if output:
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT) 

class YearAccountView(APIView):
    # List
    def get(self, request, format=None):
        account = request.query_params.get('account',None)
        if account is not None:
            account_list = DataModel.objects.values_list('account', flat=True).order_by('account').distinct()
            try:
                if int(account) in account_list:      
                    balance =  DataModel.objects.filter(account=account).values('amount').aggregate(balance = Round(Sum('amount')))['balance']
                    output = {'data': [{'account': int(account), 'balance': balance}]}
                    if balance:
                        return Response(output, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
#falta
class MonthlyView(APIView):
    # List
    def get(self, request, format=None): 
        queryset = DataModel.objects.dates('date', 'month').values('account').order_by('account').annotate(date = Substr('date', 1, 7), balance = Round(Sum('amount')))
        output = {'data': queryset}
        if output:
            return Response(output, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT) 
#falta        
class MonthlyAccountView(APIView):
    # List
    def get(self, request, format=None):
        account = request.query_params.get('account',None)
        if account is not None:
            account_list = DataModel.objects.values_list('account', flat=True).order_by('account').distinct()
            try:
                if int(account) in account_list:  
                    queryset =  DataModel.objects.filter(account=account).dates('date', 'month').values('account').annotate(date = Substr('date', 1, 7), balance = Round(Sum('amount')))
                    output = {'data': queryset}
                    if queryset:
                        return Response(output, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_204_NO_CONTENT) 
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
class MonthView(APIView):
    # List
    def get(self, request, format=None): 
        month = request.query_params.get('month',None)
        if month is not None:
            try:
                if 1 <= int(month) <= 12: 
                    queryset = DataModel.objects.filter(date__month = month).values('account').order_by('account').annotate(balance=Round(Sum('amount')))
                    output = {'data': queryset}
                    if output:
                        return Response(output, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        
class MonthAccountView(APIView):
    # List
    def get(self, request, format=None):
        account = request.query_params.get('account',None)
        month = request.query_params.get('month',None)
        if account is not None and month is not None:
            account_list = DataModel.objects.values_list('account', flat=True).order_by('account').distinct()
            try:
                if 1 <= int(month) <= 12 and int(account) in account_list:  
                    queryset =  DataModel.objects.filter(account=account, date__month=month).values('account').annotate(balance = Round(Sum('amount')))
                    output = {'data': queryset}
                    if output:
                        return Response(output, status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_204_NO_CONTENT)  
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST) 

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'