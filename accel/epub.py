from accel.inputs import Input
from accel.conversion import Conversion

class Epub(Conversion):
    KEY = 'epub'
    ALLOWED_TYPES = [
        Input.URL,
        Input.PDF,
        Input.MKD,
        Input.TXT,
        Input.EPB,
        Input.HTM
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Epub.KEY, help='Create an epub file.')
        Conversion.addParserItems(parser, Epub.ALLOWED_TYPES)
        # TODO parser.add_argument()
    @staticmethod
    def fromArgs(args):
        return Epub(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Epub, self).__init__(input, output, verbose)
        raise NotImplementedError