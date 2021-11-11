class Make(object):
    KEY = 'make'
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Make.KEY, help='Process a makefile to carry out accel builds.')
        parser.add_argument('-j', '--cores', type=int, default=1, help='Number of cores allowed.')
    @staticmethod
    def fromArgs(args):
        return Make(args.cores)
    def __init__(self, cores):
        raise NotImplementedError