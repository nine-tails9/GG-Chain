import os, boto3
import json
import random
from datetime import datetime
client = boto3.resource('dynamodb', aws_access_key_id='ASIA2FMJGGTUWI4TDAGH', aws_secret_access_key='TYl5j+L/uwVniYoQbVs4c/P4EjFXEzNNEVI/CLdO',
aws_session_token='FQoGZXIvYXdzEI3//////////wEaDIuPbbB1QkKp1P6RMyKDApPnT3C3oSHmdf+me/3hz36zGlktv97/TDdhf6R9jKG31mgU7plq1XU2Y//pbFa9A/8FXsoTobd6wqUzUxvPKlVNQm62rAPz0ybSnGSYxTQjSGxOV46e0mTthKn9flCmGBwsYG8v8pl6qwZ7ojLIAi+/xNcmfSXy+ZY9BzMAjvxtS80qnk51Mt7tdec53eldwxv5copQyUz8glGtKqqXvIh8RilMj3k+kb7PRBcL0hjj7zDxZtZ76oHt+0l+umcCPJXglhr+Z6yCUnN3EwWPAm1jlEMud2TIarkHFIam20Ozq3MxQWjVTyImeT+6XZImJR/Yk0bZfn7dTYORRwx0jJHFcIIos/yH6wU=')
data = {"id": "4", "name": "Dusty", "chainlen": 354, "acc": "84.5%"}
table = client.Table('model')
table.put_item(Item=data)
def getRequests():
    res = table.scan()
    return res['Items']
