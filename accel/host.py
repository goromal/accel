# TODO
available_hosts = ()

class Host(object):
    KEY = 'host'
    @staticmethod
    def addParserItems(subparsers):
        parser = subparsers.add_parser(Host.KEY, help='Spawn a lightweight server.')
        parser.add_argument('helper', choices=available_hosts, help='The custom server.')
    @staticmethod
    def fromArgs(args):
        return Host(helper)
    def __init__(self, helper):
        raise NotImplementedError