#! /usr/bin/env python3
import imageio.v3 as iio
from PIL import Image
import click
import extcolors


@click.command()
@click.argument('xa')
@click.argument('xe')
@click.argument('ya')
@click.argument('ye')
@click.option('-i', '--image', 'image', default='image.png',
              help='Image to be analyzed, the default image is image.png.')
@click.option('-c', '--create', 'new_file_name',
              help='Create a photo of the selected section')
def main(new_file_name, image, xa, xe, ya, ye):
    """ Welcome to the help for the "Color Extraction" script. This script allows \
        the user to extract colors from a section of an image. The results are \
        displayed in a table, where the first row contains the color in hexadecimal \
        form, the second row contains the percentage of the color in the image, \
        and the third row contains the number of pixels.

        Indicators of the boundaries of the area to be extracted are:
        xa (start in x), xe (end in x), ya (start in y) and ye (end in y).

    """
    try:

        colors, pixel_count = extcolors.extract_from_image(
            cut_arr(new_file_name, image, xa, xe, ya, ye))
        for color in colors:
            click.echo(
                'rgb {rgb} #{color} {porcent}% ({menge})'.format(
                    rgb = color[0],
                    color=rgb_to_hex(
                        color[0]),
                    porcent=100 *
                    color[1] /
                    pixel_count,
                    menge=color[1]))
    except Exception as e:
        click.echo(e)


def cut_arr(new_file_name, image, xa, xe, ya, ye):

    arr = iio.imread(r'{}'.format(image))
    #create (not save) an image-object for extcolors function..
    img = Image.fromarray(arr[int(ya):int(ye), int(xa):int(xe)], 'RGBA')
    if new_file_name:
        img.save('{}.png'.format(new_file_name))
    return img


def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


if __name__ == '__main__':
    main()
