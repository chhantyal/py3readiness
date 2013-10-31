import datetime
import logging
import os
import pprint
import re
import requests
import traceback
from urllib import urlopen
import xmlrpclib


base_url = 'http://pypi.python.org/pypi'

how_many_to_chart = 200


SESSION = requests.Session()


def req_rpc(method, *args):
    payload = xmlrpclib.dumps(args, method)

    response = SESSION.post(
        base_url,
        data=payload,
        headers={'Content-Type': 'text/xml'},
#        stream=False,
    )
    if response.status_code == 200:
        result = xmlrpclib.loads(response.content)[0][0]
        return result
    else:
        # Some error occurred
        pass


def get_package_info(name):
    release_list = req_rpc('package_releases', name, True)
    latest_version = sorted(release_list)[-1]

    downloads = 0
    generic_wheel = False
    has_wheel = False
    for release in release_list:
        for i in range(3):
            try:
                urls_metadata_list = req_rpc('release_urls', name, release)
                break
            except xmlrpclib.ProtocolError, e:
                # retry 3 times
                strace = traceback.format_exc()
                logging.error("retry %s xmlrpclib: %s" % (i, strace))

        for url_metadata in urls_metadata_list:
            if release == latest_version and url_metadata['packagetype'] == 'bdist_wheel':
                has_wheel = True
                generic_wheel = url_metadata['filename'].endswith('none-any.whl')
            downloads += url_metadata['downloads']

    # NOTE: packages with no releases or no url's just throw an exception.
    info = dict(
        downloads=downloads,
        name=name,
        wheel=has_wheel,
        generic_wheel=generic_wheel,
    )

    return info


def get_list_of_packages():
    return req_rpc('list_packages')


def get_packages():
    #package_names = ['Django', 'Pillow', 'wheel', 'tvrenamr']
    package_names = get_list_of_packages()

    for pkg in package_names:
        try:
            info = get_package_info(pkg)
        except Exception, e:
            print(pkg)
            print(e)
            continue

        print info
        yield info


def build_html(packages_list):
    total_html = '''<table><tr>
        <th>Package</th>
        <th>Downloads</th>
        <th>Wheel</th>
        <th>Generic Wheel</th>
    </tr>%s</table>'''
    rows = []
    row_template = '''
        <tr class="wheel{wheel} generic{generic_wheel}">
            <td>{name}</td>
            <td>{downloads}</td>
            <td>{wheel}</td>
            <td>{generic_wheel}</td>
        </tr>
    '''
    for package in reversed(packages_list):
        rows.append(row_template.format(**package))

    return total_html % '\n'.join(rows)


def count_good(packages_list):
    good = 0
    for package in packages_list:
        if package['wheel']:
            good += 1
    return good

def remove_irrelevant_packages(packages):
    to_ignore = 'multiprocessing', 'simplejson', 'argparse', 'uuid', 'setuptools'
    for pkg in packages:
        if pkg['name'] in to_ignore:
            continue
        else:
            yield pkg


def main():
    packages = get_packages()
    packages = remove_irrelevant_packages(packages)
    packages = list(packages)
    def get_downloads(x): return x['downloads']
    packages.sort(key=get_downloads)

    # just for backup
    open('results.txt', 'w').write(pprint.pformat(packages))

    top = packages[-how_many_to_chart:]
    html = build_html(top)

    open('results.html', 'w').write(html)

    open('count.txt', 'w').write('%d/%d' % (count_good(top), len(top)))
    open('date.txt', 'w').write(datetime.datetime.now().isoformat())


if __name__ == '__main__':
    main()

