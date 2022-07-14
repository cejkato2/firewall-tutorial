def add_flow_entry(deviceId, post_data):
    url = 'http://192.168.1.150:8181/onos/v1/flows/'
    url = url + deviceId
    headers = {'Content-type':'application/json'}
    post_message = requests.post(url,json=post_data,auth=('onos','rocks'),headers=headers)
    print(post_data)
    print(post_message) 

deviceId = "of:0000000000000001"
post_data = {"flows": [{
"priority": 50000,
"timeout": 0,
"isPermanent": true,
"deviceId": "of:00000800273f3a97",
"tableId": 0,
"tableName": "0",
"treatment": {
"instructions": [
  {
	"type": "NOACTION"    
  }
]
},
"selector": {
"criteria": [
  {
    "type": "ETH_TYPE",
    "ethType": "0x800"
  },
  {
    "type": "IPV4_SRC",
    "ip": "172.16.10.254/32"
  },
  {
    "type": "IPV4_DST",
    "ip": "172.16.10.2/32"
  }
]
}
}]}


file = open('/var/log/suricata/fast.log')
nmap_scan=[]

while 1:
  where = file.tell()
  line = file.readline()
  if not line:
    time.sleep(1)
    file.seek(where)
  else:
    print line,
    print "*"*80
    if "ET SCAN NMAP" in line:
      ipAddress = str(line.split(' ')[18].split(':')[0])
      ipAddress += "/24"            
      post_data['selector']['criteria'][0]['ip'] = str(ipAddress)      
      add_flow_entry(deviceId,post_data)
