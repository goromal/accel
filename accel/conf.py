class Conf(object):
    KEY = 'conf'
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Conf.KEY, help='Process a ConfLists.txt file to configure accel builds.')
        parser.add_argument('dir', type=str, help='Location of the ConfLists.txt file.')
    @staticmethod
    def fromArgs(args):
        return Conf(args.dir)
    def __init__(self, dir):
        raise NotImplementedError