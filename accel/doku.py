from accel.inputs import Input
from accel.conversion import Conversion

class Doku(Conversion):
    KEY = 'doku'
    ALLOWED_TYPES = [
        Input.URL,
        Input.MKD,
        Input.TXT,
        Input.EPB,
        Input.HTM,
        Input.ABC
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Doku.KEY, help='Create a DokuWiki page txt file.')
        Conversion.addParserItems(parser, Doku.ALLOWED_TYPES)
        # TODO parser.add_argument()
    def __init__(self, args):
        super(Doku, self).__init__(args)
        raise NotImplementedError