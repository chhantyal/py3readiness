import datetime
import json
import xmlrpclib

import pytz
import requests

from flags import FLAGS

from caniusepython3.pypi import all_py3_projects


BASE_URL = 'http://pypi.python.org/pypi'


SESSION = requests.Session()


def req_rpc(method, *args):
    payload = xmlrpclib.dumps(args, method)

    response = SESSION.post(
        BASE_URL,
        data=payload,
        headers={'Content-Type': 'text/xml'},
    )
    if response.status_code == 200:
        result = xmlrpclib.loads(response.content)[0][0]
        return result
    else:
        # Some error occurred
        pass


def get_json_url(package_name):
    return BASE_URL + '/' + package_name + '/json'

py3_packages = all_py3_projects()

def annotate_wheels(packages):
    print('Getting package data...')
    num_packages = len(packages)
    for index, package in enumerate(packages):
        print index + 1, num_packages, package['name']

        package['value'] = 1
        if package['name'].lower() in py3_packages:
            package['py3support'] = True
            package['css_class'] = 'success'
            package['icon'] = u'\u2713'  # Check mark
            package['title'] = 'This package supports Python 3 :)'
        else:
            package['py3support'] = False
            package['css_class'] = 'default'
            package['icon'] = u'\u2717'  # Ballot X
            package['title'] = 'This package does not support Python 3 (yet!).'


def get_top_packages():
    print('Getting packages...')
    packages = req_rpc('top_packages')
    return [{'name': n, 'downloads': d} for n, d in packages]


def remove_irrelevant_packages(packages, limit):
    print('Removing cruft...')
    added_limit = limit + len(FLAGS)
    packages = packages[:added_limit]
    
    for package in packages:
        if package['name'] in FLAGS.keys():
            packages.remove(package)

    return packages[:limit]


def save_to_file(packages, file_name):
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    with open(file_name, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%A, %d %B %Y, %X %Z'),
        }))
