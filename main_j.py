import json
import time
import requests

def get_requests(url):
    response = requests.get(url)
    if not response.ok:
        print(response.status_code)
        exit()
    return response

startTime = time.perf_counter()

# make api request to Homebrew formula info
url = 'https://formulae.brew.sh/api/formula.json'
response = get_requests(url)
packages_json = response.json()

results = list()

for package in packages_json:

    packageName = package['name']
    # get url for individual package
    package_url = f'https://formulae.brew.sh/api/formula/{packageName}.json'

    # request data for a package
    response = get_requests(package_url)
    package_json = response.json()

    # grab the data we care about--installs on request
    data = {
        'name' : package['name'],
        'desc' : package['desc'],
        'installs_on_request' : {
            '30d'  : sum(package_json['analytics']['install_on_request']['30d'].values()),
            '90d'  : sum(package_json['analytics']['install_on_request']['90d'].values()),
            '365d' : sum(package_json['analytics']['install_on_request']['365d'].values())
        },
        'installs' : {
            '30d'  : sum(package_json['analytics']['install']['30d'].values()),
            '90d'  : sum(package_json['analytics']['install']['90d'].values()),
            '365d' : sum(package_json['analytics']['install']['365d'].values())
        }
    }
    
    results.append(data)
    time.sleep(response.elapsed.total_seconds())

    print(f'{packageName} in {response.elapsed.total_seconds()} seconds')

endTime = time.perf_counter()

with open('homebrewAnalytics.json', 'w') as fOut:
    json.dump(results, fOut, indent=4)

print(f'Finished...Total time was {(endTime-startTime)} seconds for {len(packages_json)} packages')