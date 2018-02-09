import hashlib
import requests

""" CONSTANTS """
APP_VERSION = 'v1'
EXPENSES_API = '/' + APP_VERSION + '/' + 'expenses'
RING_LENGTH = 128
INPUT_JSON = {
    "id": "1",
    "name": "Foo 1",
    "email": "foo1@bar.com",
    "category": "office supplies",
    "description": "iPad for office use",
    "link": "http://www.apple.com/shop/buy-ipad/ipad-pro",
    "estimated_costs": "700",
    "submit_date": "12-10-2016"
}

hosts = ["http://localhost:5123", "http://localhost:5321", "http://localhost:5213"]
hash_ring = [0]*RING_LENGTH
hosts_id = {}


def get_hash(key):
    return long(hashlib.md5(key).hexdigest(), 16) % RING_LENGTH


def add_servers_to_ring(hosts):
    for host in hosts:
        h = get_hash(host)
        hash_ring[h] = host
        hosts_id[h] = host


def add_element(data):
    h = get_hash(data["id"])
    finder = h
    while finder not in hosts_id:
        finder += 1
        if finder == 128: finder = 0
    print("Host found: {}".format(hosts_id[finder]))
    put_to_host(hosts_id[finder], data)
    hash_ring[h] = data["id"]


def get_element(id):
    h = get_hash(id)
    finder = h
    while finder not in hosts_id:
        finder += 1
        if finder == 128: finder = 0
    print("Host found: {}".format(hosts_id[finder]))
    get_from_host(hosts_id[finder], id)


def put_to_host(host, data):
    url = host + EXPENSES_API
    print("Requesting {}".format(url))
    resp = requests.post(url, data)
    print("PUT Response: {} {}".format(resp.status_code, resp.text))


def get_from_host(host, id):
    url = host + EXPENSES_API + '/' + id
    print("Requesting {}".format(url))
    resp = requests.get(url)
    print("GET Response: {} {}".format(resp.status_code, resp.text))


add_servers_to_ring(hosts)
for i in xrange(1, 11):
    j = INPUT_JSON
    j['id'] = str(i)
    j['name'] = "Foo " + str(i)
    j['email'] = "foo" + str(i) + "@bar.com"
    j['estimated_costs'] = str(int(j['estimated_costs']) + 100)
    add_element(j)
print hash_ring
