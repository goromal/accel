from accel.utils.inputs import Input
from accel.core.conversion import Conversion

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
        parser.add_argument('--transpose', type=str, default='0', help='Transpose audio by specified number of half-steps (+/-)')
        # TODO parser.add_argument()
    @staticmethod
    def fromArgs(args):
        return Mp3(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Mp3, self).__init__(input, output, verbose)
        raise NotImplementedError