import datetime
import json

from utils import (
    annotate_wheels,
    get_top_packages,
    remove_irrelevant_packages,
)

number_to_chart = 360


def save_to_file(packages, file_name):
    now = datetime.date.today()
    with open(file_name, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%d %B %Y'),
        }))


def main():
    packages = remove_irrelevant_packages(get_top_packages(), number_to_chart)
    annotate_wheels(packages)
    save_to_file(packages, 'results.json')


if __name__ == '__main__':
    main()
