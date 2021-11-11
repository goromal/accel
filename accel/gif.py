from accel.inputs import Input
from accel.conversion import Conversion

class Gif(Conversion):
    KEY = 'gif'
    ALLOWED_TYPES = [
        Input.URL,
        Input.MP4,
        Input.AVI,
        Input.MKV,
        Input.MOV,
        Input.JPG,
        Input.PNG
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Gif.KEY, help='Create a gif file.')
        Conversion.addParserItems(parser, Gif.ALLOWED_TYPES)
        # TODO parser.add_argument()
    def __init__(self, args):
        super(Gif, self).__init__(args)
        raise NotImplementedError