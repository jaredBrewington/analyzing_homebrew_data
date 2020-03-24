import json
import requests
import time
from pprint import pprint

# making API requests to get all the package information
r = requests.get("https://formulae.brew.sh/api/formula.json")

# return success if the request went through
if r.status_code:
    print("Success! Request sent!")

packages_json = r.json()

# dumping the json into a string
packages_str = json.dumps(packages_json, indent=2)

# getting the names and description of all the packages into a list
packages_name = [packages_json[i]["name"] for i in range(len(packages_json))]
packages_desc = [packages_json[i]["desc"] for i in range(len(packages_json))]
pprint(packages_name[:5])
pprint(packages_desc[:5])
# package_url = f"https://formulae.brew.sh/api/formula/carina.json"

# r = requests.get(package_url)
# info = r.json()
# info_str = json.dumps(info, indent=2)
# print(info_str)


def get_package_information(index=0):
    """
    Function to get the package's analytics for past 30, 90 and 365 days.

    Arguments:
    ==========
    :param index: (int) Index of the package whose information is to be retrieved.
    :return: (dict) Package information containing the package name, description and installation count.
    """

    package_url = f"https://formulae.brew.sh/api/formula/{packages_name[index]}.json"

    # make API requests
    r = requests.get(package_url)

    # creating a json obect from the response
    package_json = r.json()

    # installation count
    install_requests_30 = package_json['analytics']['install_on_request']['30d'][packages_name[index]]
    install_requests_90 = package_json['analytics']['install_on_request']['90d'][packages_name[index]]
    install_requests_365 = package_json['analytics']['install_on_request']['365d'][packages_name[index]]

    install_30 = package_json['analytics']['install_on_request']['30d'][packages_name[index]]
    install_90 = package_json['analytics']['install_on_request']['90d'][packages_name[index]]
    install_365 = package_json['analytics']['install_on_request']['365d'][packages_name[index]]

    data_dict = {
        'name': packages_name[index],
        'desc': packages_desc[index],
        'install_requests_30': install_requests_30,
        'install_requests_90': install_requests_90,
        'install_requests_365': install_requests_365,
        'install_30': install_30,
        'install_90': install_90,
        'install_365': install_365
    }

    #  time to sleep before making another request
    time.sleep(r.elapsed.total_seconds())
    print("Got {0} in {1} seconds.".format(
        packages_name[index], r.elapsed.total_seconds()))

    return data_dict


# package_1 = get_package_information(0)
# print(package_1)

with open("package_info.json", "w") as f:
    t1 = time.perf_counter()
    analytics_data = list()
    for i in range(len(packages_name)):
        if packages_name[i] == 'carina':
            continue
        else:
            info_dict = get_package_information(i)
            analytics_data.append(info_dict)
            json.dump(analytics_data, f, indent=2)
    t2 = time.perf_counter()
    print("Finished in {} seconds.".format(t2 - t1))
print("done...!!")
