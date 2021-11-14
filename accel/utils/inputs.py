import os

class Input:
    ANY = 0
    URL = 1
    MP4 = 2
    AVI = 3
    MKV = 4
    MOV = 5
    JPG = 6
    PNG = 7
    GIF = 8
    PDF = 9
    SVG = 10
    TXT = 11
    MKD = 12
    EPB = 13
    HTM = 14
    MP3 = 15
    WAV = 16
    ABC = 17
    HEI = 18
    FILE_NOT_FOUND = -1
    FILE_UNRECOGNIZED = -2
    BAD_SPEC = -3

FILESPECS = {
    'mp4' : Input.MP4,
    'avi' : Input.AVI,
    'mkv' : Input.MKV,
    'mov' : Input.MOV,
    'jpg' : Input.JPG,
    'jpeg': Input.JPG,
    'png' : Input.PNG,
    'gif' : Input.GIF,
    'pdf' : Input.PDF,
    'svg' : Input.SVG,
    'txt' : Input.TXT,
    'md'  : Input.MKD,
    'epub': Input.EPB,
    'html': Input.HTM,
    'mp3' : Input.MP3,
    'wav' : Input.WAV,
    'abc' : Input.ABC,
    'heic': Input.HEI,
    '*'   : Input.ANY,
    'URL' : Input.URL
}

INPUTSTRS = {v: k for k, v in FILESPECS.items()}
INPUTSTRS[Input.URL] = 'url'

class InputSet(object):
    def __init__(self, inputs): # from args.input field
        self.items = list()
        for input in inputs:
            if 'http' in input:
                self.items.append((input, Input.URL))
                continue
            if os.path.exists(input):
                if os.path.isdir(input):
                    self._process_dir(input)
                else:
                    self._process_file(input)
            elif '\%d' in input:
                self._process_spec(input)
            else:
                self.items.append((input, Input.FILE_NOT_FOUND))
    def _process_spec(self, input):
        i = 0
        if os.path.exists(input % i):
            if os.path.isdir(input % i):
                while os.path.exists(input % i):
                    self._process_dir(input % i)
                    i += 1
            else:
                while os.path.exists(input % i):
                    self._process_file(input % i)
                    i += 1
        else:
            self.items.append((input, Input.BAD_SPEC))
    def _process_dir(self, input):
        dir_files = sorted(os.listdir(input))
        for file in dir_files:
            self._process_file(file)
    def _process_file(self, input):
        _, ext_ = os.path.splitext(input)
        ext = ext_.lower()[1:]
        try:
            self.items.append((input, FILESPECS[ext]))
        except KeyError:
            self.items.append((input, Input.FILE_UNRECOGNIZED))
