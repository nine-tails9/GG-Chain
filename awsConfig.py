import os, boto3
import json
import random
from datetime import datetime
import MySQLdb

db = MySQLdb.connect(host="database-2.c1bd8sdfacwx.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="admin",         # your username
                     passwd="electron",  # your password
                     db="database-2")

cur = db.cursor()
query = "CREATE TABLE MyGuests (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY)"
cur.execute(query)
