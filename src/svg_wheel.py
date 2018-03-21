import math
import copy
import xml.etree.ElementTree as et

from src.storage import s3_client, bucket, metadata

HEADERS = '''<?xml version=\"1.0\" standalone=\"no\"?>
<?xml-stylesheet href="wheel.css" type="text/css"?>
<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"
\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">
'''

PATH_TEMPLATE = '''
M {start_outer_x},{start_outer_y}
A{outer_radius},{outer_radius} 0 0 1 {end_outer_x},{end_outer_y}
L {start_inner_x},{start_inner_y}
A{inner_radius},{inner_radius} 0 0 0 {end_inner_x},{end_inner_y}
Z
'''

FRACTION_LINE = 80
OFFSET = 20
PADDING = 10
RADIUS = 180
CENTER = PADDING + RADIUS
TAU = 2*math.pi


def annular_sector_path(
        center_x, center_y, inner_radius, outer_radius, start, stop):
    points = {
        'inner_radius': inner_radius,
        'outer_radius': outer_radius,
        'start_outer_x': center_x + outer_radius*math.cos(start),
        'start_outer_y': center_y + outer_radius*math.sin(start),
        'end_outer_x': center_x + outer_radius*math.cos(stop),
        'end_outer_y': center_y + outer_radius*math.sin(stop),
        'start_inner_x': center_x + inner_radius*math.cos(stop),
        'start_inner_y': center_y + inner_radius*math.sin(stop),
        'end_inner_x': center_x + inner_radius*math.cos(start),
        'end_inner_y': center_y + inner_radius*math.sin(start),
    }

    return PATH_TEMPLATE.format(**points)


def add_annular_sector(
        wheel, center, inner_radius, outer_radius, start, stop, style_class):
    return et.SubElement(
        wheel, 'path',
        d=annular_sector_path(
            center_x=center[0], center_y=center[1],
            inner_radius=inner_radius, outer_radius=outer_radius,
            start=start, stop=stop,
        ),
        attrib={'class': style_class},
    )


def angles(index, total):
    start = index * TAU / total
    stop = (index + 1) * TAU / total

    return (start - TAU/4, stop - TAU/4)


def add_fraction(wheel, packages, total):
    text_attributes = {
        'text-anchor': 'middle',
        'dominant-baseline': 'central',
        'font-size': str(2*OFFSET),
        'font-family': '"Helvetica Neue",Helvetica,Arial,sans-serif',
        'fill': '#333333',
    }

    # Packages with some sort of wheel
    wheel_packages = sum(package['py3support'] for package in packages)

    packages_with_wheels = et.SubElement(
        wheel, 'text',
        x=str(CENTER), y=str(CENTER - OFFSET),
        attrib=text_attributes,
    )
    packages_with_wheels.text = '{0}'.format(wheel_packages)

    # Dividing line
    et.SubElement(
        wheel, 'line',
        x1=str(CENTER - FRACTION_LINE//2), y1=str(CENTER),
        x2=str(CENTER + FRACTION_LINE//2), y2=str(CENTER),
        attrib={'stroke': '#333333', 'stroke-width': '2'},
    )

    # Total packages
    total_packages = et.SubElement(
        wheel, 'text',
        x=str(CENTER), y=str(CENTER + OFFSET),
        attrib=text_attributes,
    )
    total_packages.text = '{0}'.format(total)


def generate_svg_wheel(packages, total):
    wheel = et.Element(
        'svg',
        viewBox='0 0 {0} {0}'.format(2*CENTER),
        version='1.1',
        xmlns='http://www.w3.org/2000/svg',
    )

    for index, result in enumerate(packages):
        start, stop = angles(index, total)
        sector = add_annular_sector(
            wheel,
            center=(CENTER, CENTER),
            inner_radius=RADIUS//2, outer_radius=RADIUS,
            start=start, stop=stop,
            style_class=result['css_class'],
        )
        title = et.SubElement(sector, 'title')
        title.text = u'{0} {1}'.format(result['name'], result['icon'])

    add_fraction(wheel, packages, total)

    tmp_wheel_path = '/tmp/wheel.svg'
    with open(tmp_wheel_path, 'w') as svg:
        svg.write(HEADERS)
        svg.write(et.tostring(wheel))

    key = 'wheel.svg'
    extra_args = copy.deepcopy(metadata)
    extra_args["ContentType"] = "image/svg+xml"

    s3_client.upload_file(tmp_wheel_path, bucket, key, ExtraArgs=extra_args)
