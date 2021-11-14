from accel.utils.inputs import Input
from accel.core.conversion import Conversion

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
    @staticmethod
    def fromArgs(args):
        return Png(args.input, args.output, args.verbose, args.height, args.width, args.screen, args.dpi)
    def __init__(self, input, output, verbose, height, width, screen, dpi):
        super(Png, self).__init__(input, output, verbose)
        raise NotImplementedError