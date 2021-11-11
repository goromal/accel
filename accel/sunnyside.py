from accel.inputs import Input
from accel.conversion import Conversion

class Sunnyside(Conversion):
    KEY = 'sunnyside'
    ALLOWED_TYPES = [
        Input.ANY
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Sunnyside.KEY, help='Change your file\'s DNA.')
        Conversion.addParserItems(parser, Sunnyside.ALLOWED_TYPES)
        parser.add_argument('-s', '--shift', type=int, help='Shift amount.')
        parser.add_argument('-k', '--key', type=str, help='Character key.')
    def __init__(self, args):
        super(Sunnyside, self).__init__(args)
        raise NotImplementedError