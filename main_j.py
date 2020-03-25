import json
import time
import requests

def get_requests(url):
    response = requests.get(url)
    if not response.ok:
        print(f'Error: {url} returned status code {response.status_code})
        exit()
    return response

start_time = time.perf_counter()

# make api request to Homebrew formula info
url = 'https://formulae.brew.sh/api/formula.json'
response = get_requests(url)
packages_json = response.json()

results = list()

for package in packages_json:

    package_name = package['name']
    # get url for individual package
    package_url = f'https://formulae.brew.sh/api/formula/{package_name}.json'

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

    print(f'{package_name} in {response.elapsed.total_seconds()} seconds')

end_time = time.perf_counter()

with open('homebrew_analytics.json', 'w') as fOut:
    json.dump(results, fOut, indent=4)

print('\nFinished...')
print(f'Total time was {(end_time-start_time)/60} minutes for {len(packages_json)} packages')