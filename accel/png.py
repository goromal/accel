from accel.inputs import Input
from accel.conversion import Conversion

class Png(Conversion):
    KEY = 'png'
    ALLOWED_TYPES = [
        Input.URL,
        Input.PNG,
        Input.JPG,
        Input.SVG,
        Input.PDF,
        Input.HEI,
        Input.MP4,
        Input.AVI,
        Input.MKV,
        Input.MOV
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Png.KEY, help='Create a png file.')
        Conversion.addParserItems(parser, Png.ALLOWED_TYPES)
        parser.add_argument('--height', type=int, default=None, help='Output height in pixels.')
        parser.add_argument('--width', type=int, default=None, help='Output width in pixels.')
        parser.add_argument('--screen', type=str, default='0:0', help='Time at which to take a screenshot (for video inputs).')
        parser.add_argument('--dpi', type=int, default=300, help='DPI for vector graphic conversions.')
    def __init__(self, args):
        super(Png, self).__init__(args)
        raise NotImplementedError