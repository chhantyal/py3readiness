import datetime
import json
import pprint

import jinja2

from utils import (
    count_good,
    get_list_of_packages,
    get_packages,
    remove_irrelevant_packages,
)

how_many_to_chart = 360


def get_from_pypi(package_names):
    packages = get_packages(package_names)
    packages = remove_irrelevant_packages(packages)
    packages = list(packages)
    def get_downloads(x): return x['downloads']
    packages.sort(key=get_downloads, reverse=True)
    return packages


def backup_to_file(packages, file_name):
    now = datetime.date.today()
    with open(file_name, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%d %B %Y'),
        }))


def chop_to_size(packages, size):
    return packages[size:]


def add_css_class(packages):
    # I wholeheartedly apologise for this display logic.
    for package in packages:
        extra = {'value': 1}
        if package['generic_wheel']:
            extra['css_class'] = 'success'
            extra['color'] = '#47a447'
        elif package['wheel']:
            extra['css_class'] = 'warning'
            extra['color'] = '#ed9c28'
        else:
            extra['css_class'] = 'danger'
            extra['color'] = '#d2322d'
        package.update(extra)


def main():
    package_names = get_list_of_packages()
    packages = get_from_pypi(package_names)
    add_css_class(packages)
    backup_to_file(packages, 'all_results.json')
    packages = chop_to_size(packages, how_many_to_chart)
    backup_to_file(packages, 'results.json')


if __name__ == '__main__':
    main()
