import copy
import datetime
import json

import caniusepython3

from src.storage import bucket, metadata, s3_client
from src.flags import FLAGS

BASE_URL = 'https://pypi.python.org/pypi'


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

    with open('top-pypi-packages.json') as data_file:
        packages = json.load(data_file)['rows']

    # Rename keys
    for package in packages:
        package['downloads'] = package.pop('download_count')
        package['name'] = package.pop('project')

    return packages


def remove_irrelevant_packages(packages, limit):
    print('Removing cruft...')
    added_limit = limit + len(FLAGS)
    packages = packages[:added_limit]

    packages = [package for package in packages
                if package.get('name') not in FLAGS.keys()]

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

    try:
        s3_client.upload_file(tmp_path, bucket, key, ExtraArgs=extra_args)
    except Exception as e:
        print(e)
