from accel.utils.inputs import Input
from accel.core.conversion import Conversion

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
    @staticmethod
    def fromArgs(args):
        return Doku(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Doku, self).__init__(input, output, verbose)
        raise NotImplementedError