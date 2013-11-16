import math
import xml.etree.ElementTree as et


TAU = 2*math.pi


def add_headers(f):
    f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
    f.write('<?xml-stylesheet href="wheel.css" type="text/css"?>')
    f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
    f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')


def annular_sector_path(center_x, center_y, inner_radius, outer_radius, start, stop):
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

    path_d = ' '.join((
        'M {start_outer_x},{start_outer_y}',
        'A{outer_radius},{outer_radius} 0 0 1 {end_outer_x},{end_outer_y}',
        'L {start_inner_x},{start_inner_y}',
        'A{inner_radius},{inner_radius} 0 0 0 {end_inner_x},{end_inner_y}',
        'Z',
    ))

    return path_d.format(**points)


def add_annular_sector(wheel, center, inner_radius, outer_radius, start, stop, style_class):
    et.SubElement(wheel, 'path',
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


def generate_svg_wheel(packages, total):
    wheel = et.Element('svg', width='380', height='380', version='1.1', xmlns='http://www.w3.org/2000/svg')

    for index, result in enumerate(packages):
        start, stop = angles(index, total)
        add_annular_sector(
            wheel,
            center=(190, 190),
            inner_radius=90, outer_radius=180,
            start=start, stop=stop,
            style_class=result['css_class'],
        )

    # Packages with some sort of wheel
    wheel_packages = len([1 for package in packages if package['wheel']])

    wheels = et.SubElement(wheel, 'text',
        x='190', y='190',
        attrib = {'text-anchor': 'middle', 'font-size': '40', 'dominant-baseline': 'central'},
    )
    wheels.text='{}/{}'.format(wheel_packages, total)

    with open('wheel.svg', 'w') as svg:
        add_headers(svg)
        svg.write(et.tostring(wheel))

