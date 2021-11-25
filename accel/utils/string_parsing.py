import re

def hhmmss_from_str(hhmmss_str):
    searchres = re.search(r'((\d\d*):)?(\d\d*):(\d\d*\.?\d*)', hhmmss_str)
    if searchres:
        groups = searchres.groups()
        hh = int(groups[1]) if groups[1] is not None else 0
        mm = int(groups[2])
        ss = float(groups[3])
    else:
        raise Exception('Provided time string (%s) does not have the correct format.' % hhmmss_str)
    return hh, mm, ss