from accel.inputs import Input
from accel.conversion import Conversion

class Pdf(Conversion):
    KEY = 'pdf'
    ALLOWED_TYPES = [
        Input.URL,
        Input.PDF,
        Input.SVG,
        Input.MKD,
        Input.TXT,
        Input.EPB,
        Input.HTM,
        Input.JPG,
        Input.PNG,
        Input.ABC
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Pdf.KEY, help='Create a pdf file.')
        Conversion.addParserItems(parser, Pdf.ALLOWED_TYPES)
        # TODO parser.add_argument()
    def __init__(self, args):
        super(Pdf, self).__init__(args)
        raise NotImplementedError