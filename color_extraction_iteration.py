#! /usr/bin/env python3

import imageio.v3 as iio
from PIL import Image
import click
import extcolors
import json
import os


@click.command()
@click.argument('xa',type=int)
@click.argument('xe',type=int)
@click.argument('ya',type=int)
@click.argument('ye',type=int)
@click.option('-p', '--path', 'path', default='images',
              help='??????')
@click.option('-n', '--name', 'new_file_name', default='results',
              help='??????')
def main(new_file_name, path, xa, xe, ya, ye):
    """ Welcome to the help for the "Color Extraction" script. This script allows \
        the user to extract colors from multiple images.  The results are displayed \
        in a table, where the first row contains the color in hexadecimal form, the \
        second row contains the percentage of the color in the image, and the third \
        row contains the number of pixels.

        Indicators of the boundaries of the areas are: xa (start in x), xe (end in \
        x), ya (start in y), and ye (end in y).
    """

    data = []
    try:
        for file_path, file_name in iterate_files(r'{}'.format(path)):
            img = new_img(file_path, xa, xe, ya, ye)
            data.append(metadata(file_name, img))
        if os.path.exists('{}.json'.format(new_file_name)):
            os.remove('{}.json'.format(new_file_name))
        with open('{}.json'.format(new_file_name), 'a') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))

    except Exception as e:
        click.echo(e)


def colors_f(colors, pixel_count):
    arr = []
    for color in colors:
        arr.append('{rgb} #{color} {porcent}% ({menge})'.format(
            rgb=color[0],
            color='%02x%02x%02x' % color[0],
            porcent=100 * color[1] / pixel_count,
            menge=color[1]))
    return arr


def iterate_files(it_path):
    for root, _, files in os.walk(it_path):
        for file in files:
            yield os.path.abspath(os.path.join(root, file)), file


def new_img(file_path, xa, xe, ya, ye):
    arr = iio.imread(r'{}'.format(file_path))
    return Image.fromarray(arr[ya:ye, xa:xe], 'RGBA')


def metadata(file_name, img):
    metadata = file_name.split('_')
    colors, pixel_count = extcolors.extract_from_image(img)
    if len(metadata) == 3:
        metadata.insert(1, 'stadt')
    data = {
        'Date': metadata[2],
        'Timestamp': metadata[3].split('.')[0],
        'Source': metadata[0],
        'Location': metadata[1],
        'results': colors_f(colors, pixel_count)
    }
    return data


if __name__ == '__main__':
    main()
