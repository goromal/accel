from accel.inputs import Input
from accel.conversion import Conversion

class Html(Conversion):
    KEY = 'html'
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
        parser = subparsers.add_parser(Html.KEY, help='Create an html file.')
        Conversion.addParserItems(parser, Html.ALLOWED_TYPES)
        # TODO parser.add_argument()
    @staticmethod
    def fromArgs(args):
        return Html(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Html, self).__init__(input, output, verbose)
        raise NotImplementedError