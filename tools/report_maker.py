#!/usr/bin/python3
import pymysql.cursors
def createCon():
  connection = pymysql.connect(host='localhost',
                             user='prettycool',
                             password='FRESHINSTALL',
                             db='db_data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
  return connection


def execQuery(query):
  connection = createCon()
  with connection.cursor() as cursor:
    cursor.execute(query)
    result=cursor.fetchall()
    connection.close()
    if len(result) > 0:
      return result

def listDomains():
  # Query all domains in the database; 
  query = "select domainName,createdAt from tb_domain;" 
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      print(result[domain]['domainName'])
  
def hostOnly(hostname):
  # Query all domains in the database; 
  query = "select hostname,port from tb_port where hostname = '{}'; ".format(hostname)
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      print(result[domain]['domainName'])

def hostsFromDomain(domain):
  count=0
  print("[+] Hosts from Domain {}:".format(domain))
  # Total de hosts localizados para o dominio.
  query="select count(hostName) as total from tb_host where domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    totalHosts=result[0]['total']
  query="select count(hostName) as total from tb_host where ipAddress != 'False' and domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    totalValidHosts=result[0]['total']
  missing=totalHosts-totalValidHosts
  print("[-] For Domain {}  we have {} hostnames but only {}  has valid IPv4. Hosts missing IPv4: {}".format(domain,totalHosts,totalValidHosts,missing))
  #query ="select tb_host.hostName,tb_host.ipAddress,tb_port.port, tb_port.protocol,tb_port.banner from tb_host inner join tb_port where tb_host.domainName='{}' and tb_port.ipAddress = tb_host.ipAddress order by 1;".format(domain)
  query ="select hostName,ipAddress from tb_host where domainName='{}' and ipAddress != 'False' order by 1;".format(domain)
  result = execQuery(query)
  if result:
    for host in range(len(result)):
      ipAddress=result[host]['ipAddress']
      hostName=result[host]['hostName']
      print("[=] Hostname: {} ipAddress: {}".format(hostName,ipAddress))
      query ="select port,protocol,banner from tb_port where hostName = '{}' order by 1;".format(hostName)
      resultPorts = execQuery(query)
      if resultPorts:
        for port in range(len(resultPorts)):
          protocol=resultPorts[port]['protocol']
          rport=resultPorts[port]['port']
          banner=resultPorts[port]['banner']
          if banner.decode() == 'Null':
            print("\t\tPort: {} STATUS OPEN Protocol: {} Banner: None ".format(rport,protocol))
          else:
            print("\t\tPort: {} STATUS OPEN Protocol: {} \n\t\t\t\tBanner: ".format(rport,protocol))
            line=''
            for w in banner.decode():
              line+=''.join(w)
              if w == '\n':
                lineprint='\t\t\t\t\t'+line
                print(lineprint.replace('\r','').replace('\n',''))
                line=''

      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} records in database".format(count))

def relatedDomains(domain):
  count=0
  print("[+] Related domains from from Domain {}:".format(domain))
  query ="select domainName from tb_relatedDomains where mainDomain ='{}';".format(domain)
  result = execQuery(query)
  if result:
    for domain in range(len(result)):
      rdomain=result[domain]['domainName']
      print("\t[-] Related Domain: {}".format(rdomain))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} related Domains in database".format(count))

def pastebin(domain):
  count=0
  print("[+] Pastebin related with domain {}:".format(domain))
  query ="select url,title,dumpDate from tb_pastebin where domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    for paste in range(len(result)):
      url=result[paste]['url']
      title=result[paste]['title']
      dumpDate=result[paste]['dumpDate']
      print("\t[-] URL: {} DumpDate: {} Title: {} ".format(url,dumpDate,title))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} links in database".format(count))

def buckets(domain):
  count=0
  print("[+] Buckets from Domain {}:".format(domain))
  query ="select url from tb_aws where domainName='{}';".format(domain)
  result = execQuery(query)
  if result:
    for url in range(len(result)):
      print("\t[-] Bucket: {}".format(result[url]['url']))
      count+=1
  else:
    print("[+] {} Not found in database".format(domain))
  print("[!] Found {} Buckets in database".format(count))

def makeReport(domain):
  pastebin(domain)
  buckets(domain)
  hostsFromDomain(domain)
  relatedDomains(domain)

if __name__ == "__main__":
  import sys
  domain_name = sys.argv[1]
  makeReport(domain_name)
  #hostsFromDomain(domain_name)
  #buckets(domain_name)
  #relatedDomains(domain_name)
  #listDomains()
  #hostOnly(domain_name)
