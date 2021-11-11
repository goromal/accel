import inputs

class Conversion(object):
    @staticmethod
    def addParserItems(parser, allowed_types):
        allowed_strs = [inputs.INPUTSTRS[atype] for atype in allowed_types]
        parser.add_argument('input', nargs='*', help='Input(s). Supported: %s.' % ', '.join(allowed_strs))
        parser.add_argument('-o', '--output', type=str, default='output', action='store', help='Specify output filename')
    def __init__(self, args):
        self.inputs = inputs.InputSet(args.input).items