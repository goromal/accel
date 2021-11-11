from accel.inputs import Input
from accel.conversion import Conversion

class Mp4(Conversion):
    KEY = 'mp4'
    ALLOWED_TYPES = [
        Input.URL,
        Input.MP4,
        Input.AVI,
        Input.MKV,
        Input.MOV
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Mp4.KEY, help='Create an mp4 file.')
        Conversion.addParserItems(parser, Mp4.ALLOWED_TYPES)
        # TODO parser.add_argument()
    def __init__(self, args):
        super(Mp4, self).__init__(args)
        raise NotImplementedError