from accel.utils.inputs import Input
from accel.core.conversion import Conversion

class Zip(Conversion):
    KEY = 'zip'
    ALLOWED_TYPES = [
        Input.ANY
    ]
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Zip.KEY, help='Create a zipped archive.')
        Conversion.addParserItems(parser, Zip.ALLOWED_TYPES)
        parser.add_argument('-u', '--unzip', action='store_true', help='Unzip a zipped archive.')
    @staticmethod
    def fromArgs(args):
        return Zip(args.input, args.output, args.verbose) # TODO
    def __init__(self, input, output, verbose):
        super(Zip, self).__init__(input, output, verbose)
        raise NotImplementedError
