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
    def __init__(self, args):
        super(Html, self).__init__(args)
        raise NotImplementedError