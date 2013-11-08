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
    with open(file_name, 'w') as f:
        f.write(json.dumps({'data': packages}))


def chop_to_size(packages, size):
    return packages[-size:]


def add_css_class(packages):
    # I wholeheartedly appologise for this display logic.
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

def build_html(packages):
    with open('html_template.html', 'r') as input_file:
        template = jinja2.Template(input_file.read())

    return template.render(
        title='Python Wheel of Shame',
        packages=packages,
    )



def main():
    package_names = get_list_of_packages()
    packages = get_from_pypi(package_names)
    packages = chop_to_size(packages, how_many_to_chart)
    add_css_class(packages)
    backup_to_file(packages, 'results.json')

    html = build_html(packages)

    open('results.html', 'w').write(html)

    open('date.txt', 'w').write(datetime.datetime.now().isoformat())


if __name__ == '__main__':
    main()

