# Django
from django.test import TestCase
from django.urls import reverse

# Django Rest Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Models
from .models import DataModel

# Python
import json
import datetime

class MyAPITestCase(APITestCase):
    def test_data(self):
        url_data = reverse('data')
        
        response_users = self.client.post(url_data, self.get_json('2020-03-20', 120001, 500), format='json')
        self.assertEqual(response_users.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataModel.objects.count(), 1)
        self.assertEqual(DataModel.objects.get().date, datetime.date(2020, 3, 20))
        self.assertEqual(DataModel.objects.get().account, 120001)
        self.assertEqual(DataModel.objects.get().amount, 500.0)
        
    def test_year(self):
        # Inserting data to test
        url_data = reverse('data')
            
        response_data = self.client.post(url_data, self.get_data(), format='json')
        self.assertEqual(response_data.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataModel.objects.count(), 6)
        
        # Testing /year
        url_year = reverse('year')
        check_resp_year = {
            'data': [
                {
                    'account': 120001,
                    'balance': 800.0
                },
                {
                    'account': 120002,
                    'balance': 900.0
                }
            ]
        }
        
        response_year = self.client.get(url_year, format='json')
        result_year = json.loads(response_year.content)
        self.assertEqual(result_year, check_resp_year)
        
        # Testing /yearaccount
        check_resp_yearaccount = {
            'data': [
                {
                    'account': 120001,
                    'balance': 800.0
                }
            ]
        }
        
        response_yearaccount = self.client.get('/api/yearaccount?account=120001')
        result_yearaccount = json.loads(response_yearaccount.content)
        self.assertEqual(result_yearaccount, check_resp_yearaccount)
        
    def test_monthly(self):
        # Inserting data to test
        url_data = reverse('data')
            
        response_data = self.client.post(url_data, self.get_data(), format='json')
        self.assertEqual(response_data.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataModel.objects.count(), 6)
        
        # Testing /monthly
        url_monthly = reverse('monthly')
        check_resp_monthly = {
            'data': [
                {'account': 120001, 'date': '2020-03', 'balance': 700.0}, 
                {'account': 120001, 'date': '2020-06', 'balance': 700.0}, 
                {'account': 120001, 'date': '2020-08', 'balance': -600.0}, 
                {'account': 120002, 'date': '2020-10', 'balance': 900.0}
            ]
        }
        
        response_monthly = self.client.get(url_monthly, format='json')
        result_monthly = json.loads(response_monthly.content)
        self.assertEqual(result_monthly, check_resp_monthly)
        
        # Testing /monthlyaccount
        check_resp_monthlyaccount = {
            'data': [
                {'account': 120001, 'date': '2020-03', 'balance': 700.0}, 
                {'account': 120001, 'date': '2020-06', 'balance': 700.0}, 
                {'account': 120001, 'date': '2020-08', 'balance': -600.0}
            ]
        }
        
        response_monthlyaccount = self.client.get('/api/monthlyaccount?account=120001')
        result_monthlyaccount = json.loads(response_monthlyaccount.content)
        self.assertEqual(result_monthlyaccount, check_resp_monthlyaccount)
        
    def test_month(self):
        # Inserting data to test
        url_data = reverse('data')
            
        response_data = self.client.post(url_data, self.get_data(), format='json')
        self.assertEqual(response_data.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataModel.objects.count(), 6)
        
        # Testing /month
        check_resp_month = {
            'data': [
                {
                    'account': 120001, 
                    'balance': -600.0
                }
            ]
        }
        
        response_month = self.client.get('/api/month?month=8', format='json')
        result_month = json.loads(response_month.content)
        self.assertEqual(result_month, check_resp_month)
        
        # Testing /monthaccount
        check_resp_monthaccount = {
            'data': [
                {
                    'account': 120001,
                    'balance': 700.0
                }
            ]
        }
        
        response_monthaccount = self.client.get('/api/monthaccount?account=120001&month=3')
        result_monthaccount = json.loads(response_monthaccount.content)
        self.assertEqual(result_monthaccount, check_resp_monthaccount)
        
    def get_json(self, date, account, amount):
        json = {
            'date': date,
            'account': account,
            'amount': amount
        }
        return json
    
    def get_data(self):
        data = [
            self.get_json('2020-03-20', 120001, 500),
            self.get_json('2020-10-24', 120002, -300),
            self.get_json('2020-03-12', 120001, 200),
            self.get_json('2020-06-02', 120001, 700),
            self.get_json('2020-10-30', 120002, 1200),
            self.get_json('2020-08-15', 120001, -600),
        ]
        return data
