from accel.utils.inputs import Input
from accel.core.conversion import Conversion

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
        parser.add_argument('-q', '--quality', dest='quality', type=int,      default=-1,  action='store', help='Give a number (24-30), lower is higher quality.')
        parser.add_argument('-w', '--width',   dest='width',   type=int,      default=-1,  action='store', help='Desired width (in pixels) of output video.')
        parser.add_argument('-l', '--label',   metavar=None, dest='label',   type=str,      nargs=2,     default=['__NULL__','-1'], action='store', help='e.g., "My Label" 24 ... Add label (with fontsize) to bottom left corner of video.')
        parser.add_argument('-c', '--crop',    metavar=None, dest='crop',    type=int,      nargs=4,     default=[None,None,None,None], action='store', help='X Y W H ... Applied BEFORE any labeling or resizing.') 
        parser.add_argument('-s', '--start',   dest='start',   type=str,      default='-', action='store', help='INITIAL time: [HH:]MM:SS[.0]')
        parser.add_argument('-e', '--end',     dest='end',     type=str,      default='-', action='store', help='FINAL time: [HH:]MM:SS[.0]')
    @staticmethod
    def fromArgs(args):
        return Mp4(args.input, args.output, args.verbose, args.quality, args.width, args.label, args.crop, args.start, args.end) # TODO
    def __init__(self, input, output, verbose, quality, width, label, crop, start, end):
        super(Mp4, self).__init__(input, output, verbose)
        raise NotImplementedError