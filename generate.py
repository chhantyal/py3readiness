from src.svg_wheel import generate_svg_wheel
from src.utils import (
    annotate_wheels,
    get_top_packages,
    remove_irrelevant_packages,
    save_to_file,
)


TO_CHART = 360


def main(*args):
    packages = remove_irrelevant_packages(get_top_packages(), TO_CHART)
    annotate_wheels(packages)
    save_to_file(packages)
    generate_svg_wheel(packages, TO_CHART)


if __name__ == '__main__':
    main()
