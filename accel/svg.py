from accel.inputs import Input
from accel.conversion import Conversion

class Svg(Conversion):
    KEY = 'svg'
    ALLOWED_TYPES = [
        Input.URL,
        Input.PDF,
        Input.SVG,
        Input.ABC
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Svg.KEY, help='Create an svg file.')
        Conversion.addParserItems(parser, Svg.ALLOWED_TYPES)
        parser.add_argument('--scour', action='store_true', help='Apply Jeff Schiller\'s and Lous Simard\'s Scour program to optimize file size.')
        parser.add_argument('--rmtext', action='store_true', help='Remove all text elements from the output.')
        parser.add_argument('--rmwhite', action='store_true', help='Remove all white elements from the output.')
        parser.add_argument('--poppler', action='store_true', help='Convert using Poppler fonts where applicable.')
        parser.add_argument('--crop', action='store_true', help='Crop output to content.')
    def __init__(self, args):
        super(Svg, self).__init__(args)
        raise NotImplementedError