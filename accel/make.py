class Make(object):
    KEY = 'make'
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Make.KEY, help='Process a makefile to carry out accel builds.')
        parser.add_argument('-j', '--cores', type=int, default=1, help='Number of cores allowed.')
    def __init__(self, args):
        raise NotImplementedError