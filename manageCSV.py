# Python
import pandas as pd
import mysql.connector
import time
import os

# Django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

#### FUNCTIONS
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
 
#### BODY
flag1=0
while(flag1 != 'yes' and flag1 != 'no'):
    flag1 = input('Do you want to create the database abacum?: Please type yes or no: ').lower()

if flag1 == 'yes':
    # Create database and set privileges to myuser
    pw = input('Please, insert your password for user root in MySQL: ')
    conn, cursor = conexionMysql('localhost', 'root', pw)
    cursor.execute('CREATE DATABASE abacum CHARACTER SET utf8mb4')
    cursor.execute('CREATE USER myuser@localhost IDENTIFIED BY "pass"')
    cursor.execute('GRANT ALL PRIVILEGES ON abacum.* TO myuser@localhost')
    cursor.execute('GRANT ALL PRIVILEGES ON test_api.* TO myuser@localhost')
    cursor.execute('FLUSH PRIVILEGES')
    desconexionMysql(conn, cursor)
    print('Database and user created')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Abacum.settings")
    application = get_wsgi_application()
    call_command("makemigrations", interactive=False)
    call_command("migrate", interactive=False)

flag2=0
while(flag2 != 'yes' and flag2 != 'no'):
    flag2 = input('Do you want to import the data from CSV to database abacum?: Please type yes or no: ').lower()

if flag2 == 'yes':
    # Get CSV data
    csv_data = pd.read_csv('https://raw.githubusercontent.com/abacum-io/abacum-recruitment-test/master/backed-python/support-files/sample-data.csv',
                            index_col=False)
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