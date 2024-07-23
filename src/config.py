import urllib
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True # Turns on debugging features in Flask สำหรับเปิด debug
JSON_SORT_KEYS = False #การเรียง JSON
SQLALCHEMY_TRACK_MODIFICATIONS = False # ปิด Warning

# Localhost
# params = urllib.parse.quote_plus("DRIVER={SQL Server};Server=192.168.112.10;PORT=1433;Database=BETASK_LOYALTY;UID=sa;PWD=10143;") 
 # Windows Server
 # params = urllib.parse.quote_plus("DRIVER={SQL Server};Server=192.168.112.10;PORT=1433;Database=BETASK_LOYALTY;UID=sa;PWD=10143;")
 
# Mysql
# params = "mysql+mysqlconnector://root:P@$$vv0rd@223.27.212.102:9212/BETASK_LOYALTY"
# params = "mysql+mysqlconnector://Production_Loyalty:gtEUXc=v7N@192.168.112.20:3306/BETASK_LOYALTY"
# Docker Server Vgroup
params = os.getenv('MYSQL_CONNECTION')
# params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};Server=192.168.112.10;PORT=1433;Database=BETASK_LOYALTY;UID=sa;PWD=10143;TDS_Version=8.0;")
 # Docker Server local
 # params = urllib.parse.quote_plus("DRIVER={FreeTDS};Server=192.168.112.10;PORT=1433;Database=BETASK_LOYALTY;UID=sa;PWD=10143;TDS_Version=8.0;")

# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params

SQLALCHEMY_DATABASE_URI = params
# SQLALCHEMY_DATABASE_URI = 'sqlite:///posts.db'