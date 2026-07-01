import json, urllib.request, sys

TOKEN = sys.argv[1]

req = urllib.request.Request('https://api.github.com/')
req.add_header('Authorization', f'token {TOKEN}')
req.add_header('Accept', 'application/vnd.github.v3+json')

resp = urllib.request.urlopen(req)
scopes = resp.headers.get('X-OAuth-Scopes', 'none')
print('Scopes:', scopes)

# Check repo
req2 = urllib.request.Request('https://api.github.com/repos/qppd/coin-changer')
req2.add_header('Authorization', f'token {TOKEN}')
req2.add_header('Accept', 'application/vnd.github.v3+json')

try:
    resp2 = urllib.request.urlopen(req2)
    repo = json.loads(resp2.read())
    print('Repo:', repo['full_name'])
    print('Private:', repo['private'])
except urllib.error.HTTPError as e:
    print(f'Repo check: {e.code} - {e.reason}')
    if e.code == 404:
        print('Repo NOT found! Need to create it.')
