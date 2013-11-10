import logging
import requests
import traceback
import xmlrpclib
from distutils.version import LooseVersion


base_url = 'http://pypi.python.org/pypi'


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


def get_package_versions(package_name):
    versions = req_rpc('package_releases', package_name, True)
    return sorted(versions, key=LooseVersion)


def get_package_info(package_name):
    release_list = get_package_versions(package_name)
    latest_version = release_list[-1]

    downloads = 0
    generic_wheel = False
    has_wheel = False
    for release in release_list:
        for i in range(3):
            try:
                urls_metadata_list = req_rpc('release_urls', package_name, release)
                break
            except xmlrpclib.ProtocolError:
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
        name=package_name,
        wheel=has_wheel,
        generic_wheel=generic_wheel,
    )

    return info


def get_list_of_packages():
    return req_rpc('list_packages')


def get_packages(package_names):
    for pkg in package_names:
        try:
            info = get_package_info(pkg)
        except Exception as e:
            print(pkg)
            print(e)
            continue

        print(info)
        yield info


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
