from accel.inputs import Input
from accel.conversion import Conversion

class Mp3(Conversion):
    KEY = 'mp3'
    ALLOWED_TYPES = [
        Input.URL,
        Input.MP4,
        Input.AVI,
        Input.MKV,
        Input.MOV,
        Input.MP3,
        Input.WAV,
        Input.ABC
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Mp3.KEY, help='Create an mp3 file.')
        Conversion.addParserItems(parser, Mp3.ALLOWED_TYPES)
        # TODO parser.add_argument()
    def __init__(self, args):
        super(Mp3, self).__init__(args)
        raise NotImplementedError