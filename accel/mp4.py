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
    @staticmethod
    def fromArgs(args):
        return Mp4(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Mp4, self).__init__(input, output, verbose)
        raise NotImplementedError