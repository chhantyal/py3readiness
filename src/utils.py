import copy
import datetime
import json
import xmlrpclib

import caniusepython3
import requests

from src.storage import bucket, metadata, s3_client
from src.flags import FLAGS

SESSION = requests.Session()
BASE_URL = 'https://pypi.python.org/pypi'


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


def annotate_wheels(packages):
    print('Getting package data...')
    num_packages = len(packages)
    for index, package in enumerate(packages):
        print(index + 1, num_packages, package['name'])

        package['value'] = 1
        if caniusepython3.check(projects=[package['name']]):
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

    packages = [package for package in packages if package.get('name') not in FLAGS.keys()]

    return packages[:limit]


def save_to_file(packages):
    now = datetime.datetime.now()
    key = 'results.json'
    tmp_path = '/tmp/{0}'.format(key)
    with open(tmp_path, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%A, %d %B %Y, %X %Z'),
        }))

    extra_args = copy.deepcopy(metadata)
    extra_args["ContentType"] = "application/json"

    s3_client.upload_file(tmp_path, bucket, key, ExtraArgs=extra_args)
