from accel import inputs
from colorama import Fore, Style

class Conversion(object):
    @staticmethod
    def addParserItems(parser, allowed_types):
        allowed_strs = [inputs.INPUTSTRS[atype] for atype in allowed_types]
        parser.add_argument('input', nargs='*', help='Input(s). Supported: %s.' % ', '.join(allowed_strs))
        parser.add_argument('-o', '--output', type=str, default='output', action='store', help='Specify output filename')
    def __init__(self, input, output, verbose):
        self.inputs = inputs.InputSet(input).items
        self.output = output
        self.verbose = verbose
    def printError(self, s):
        print(Fore.RED + s + Style.RESET_ALL)
        exit()
    def printInfo(self, s):
        if self.verbose:
            print(s)