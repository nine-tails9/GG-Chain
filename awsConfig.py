import os, boto3
import json
import random
from datetime import datetime
random.seed(datetime.now())
dynamodb = boto3.resource('dynamodb', aws_access_key_id='ASIA2FMJGGTU5ZBVPQLU', aws_secret_access_key='4wete1JBzMLqJdeFVGm10IBkOhDZ2bf82n6Ns2M9',
aws_session_token='FQoGZXIvYXdzEIf//////////wEaDHT+t8bxgITzOvcqaCKDAg+mqkkWVtiHqJPOYuYFShSZoLGE5pvDaD1HEv5iRfi0OXN0hpLtZ6lcNY/GZ0RefkLUsZPxVhS5gK99vrrhCBwuvL9GGP2nD9eXys5RgTNaiKIA9TX9K+prVmzCVdpgz5BacLNT8cZZWktQneTnBrbP/ZrPf5DSUr43dSS2l0dSH7U24OR5jv+cB9ERgz1U3LqTlDqCAob+e3ways+ZAu66QNeuPkQ2X2li1tLQlOONqzZJGfiG21l8ADSPttUhZFVwsrkG4a1lTvT3CXvDbp/u2f+00ykmhGZ8m9pvQ4HKfRaD5SL61mvXsQMhsURCBkTcytU3eA2BS+g+PNDLejMi2pgoj82G6wU=')
data = {
                "id": str(random.randrange(1, 100000000)),
                "noe": "mnee"
        }
table = dynamodb.Table('models')
table.put_item(Item=data)
