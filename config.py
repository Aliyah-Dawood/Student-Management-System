# config.py
DB_CONFIG = {
    'server': r'DESKTOP-RONHFA7\SQLEXPRESS',        # Example: localhost\SQLEXPRESS
    'database': 'student_performance',
    'driver': 'ODBC Driver 17 for SQL Server'  # Or 18 if installed
}
import pyodbc
print(pyodbc.drivers())
