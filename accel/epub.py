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
    def __init__(self, args):
        super(Epub, self).__init__(args)
        raise NotImplementedError