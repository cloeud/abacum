# Rest Framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Django
from .models import CSVModel
from api.models import DataModel
from .serializers import CSVSerializer

# Python
import time
import pandas as pd
import mysql.connector

class CSVView(APIView):
    # List
    def get(self,request):
        data = CSVModel.objects.all()
        serializer = CSVSerializer(data, many=True)      
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create
    def post(self,request):
        start = time.time()
        serializer = CSVSerializer(data=request.data)
        if serializer.is_valid():
            # All data objects will be deleted before load data from CSV
            queryset = DataModel.objects.all().delete()
            # CSV data will be downloaded and set into our DataModel structure
            csv_url = serializer.validated_data["url"]
            csv_data = pd.read_csv(csv_url, index_col=False)
            csv_data.head() 
            # Insert CSV data into database abacum
            conn, cursor = conexionMysql('localhost', 'myuser', 'pass', 'abacum')
            try:
                cursor.execute('TRUNCATE TABLE transactions')
                start = time.time()
                j = 0
                print('Inserting all data...')
                for i, row in csv_data.iterrows():
                    j += 1
                    sql = f'INSERT INTO abacum.transactions VALUES ({i+1},%s,%s,%s)'
                    cursor.execute(sql, tuple(row))
                    if j % 1000 == 0 and j > 999:
                        conn.commit()
                end = time.time()
                result = end - start
                print('All data was inserted in {0:.2f} seconds'.format(result))
            except mysql.connector.Error as e: 
                if e.errno == 1146:
                    print("Table transactions doesn't exists {} ".format(e.errno))	
                else:
                    print("ERROR: " + str(e))
            desconexionMysql(conn, cursor)
            end = time.time()
            print(end-start)
            return Response({"message": "CSV content was perfectly loaded into data"},status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid URL field, it must be a CSV file"},status=status.HTTP_400_BAD_REQUEST)
    
class CSVDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CSVModel.objects.all()
    serializer_class = CSVSerializer
    
def conexionMysql(DB_HOST, DB_USER, DB_PASS, DB=None):
	flag = False
	n_try_max = 50
	n_sec_try = 60
	n_try = 0
	while((flag == False) and (n_try < n_try_max)):
		try:
			n_try += 1
			conn_servidor = mysql.connector.connect(host=DB_HOST, database = DB, user = DB_USER, password = DB_PASS)
			cursor_servidor = conn_servidor.cursor()
			flag = True
		except mysql.connector.Error as e:

			if e.errno == 2013 or e.errno == 2003:
				print("Erro trying to connect. Retrying. Error code {} ".format(e.errno))
			else:
				print("ERROR: " + str(e))
			flag = False
			time.sleep(n_sec_try)

	return conn_servidor, cursor_servidor

def desconexionMysql(conn_servidor, cursor_servidor):
	cursor_servidor.close()
	conn_servidor.close()