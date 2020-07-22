import http.client

conn = http.client.HTTPConnection("prism-central.chambly.grothe.local")

payload = "{\"kind\":\"cluster\",\"length\":100}"

headers = {
    'content-type': "application/json",
    'accept': "application/json",
    'authorization': "Basic YWRtaW46Tm90NFlhMDMh"
    }

conn.request("POST", "/api/nutanix/v3/clusters/list", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))