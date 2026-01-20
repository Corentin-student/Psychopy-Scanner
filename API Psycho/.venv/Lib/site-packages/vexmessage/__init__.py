import json as _json
import textwrap as _textwrap


VERSION = '0.4.0'

class Message:
    def __init__(self,
                 target: str,
                 source: str,
                 uuid: str,
                 version: str=VERSION,
                 **content):
        """
        target -> where this message is to go
        source -> string representation of where it's from 
        uuid -> UUID
        """

        self.target = target
        self.source = source
        self.uuid = uuid
        self.VERSION = version
        self.contents = content

    def __repr__(self):
        s = "type: {}  target: {}  source: {}  version: {}  contents: {}"
        target = self.target
        if target == '':
            target = 'all'
        s = s.format(target,
                     self.source,
                     self.VERSION,
                     self.contents)

        return _textwrap.fill(s)

def decode(frame) -> Message:
    target = frame[0].decode('utf8')
    deserial = _json.loads(frame[1].decode('utf8'))
    source = deserial[0]
    uuid = deserial[1]
    version = deserial[2]
    content = deserial[3]

    return Message(target, source, uuid, version, **content)


def encode(target: str,
           source: str,
           uuid: str,
           version: str=VERSION,
           **message) -> tuple:

    target = target.encode('utf8')
    serialization = _json.dumps((source, uuid, version, message)).encode('utf8')
    return (target, serialization)


def create_vex_message(target: str,
                       source: str,
                       uuid: str,
                       version: str=VERSION,
                       **msg) -> Message:

    return encode(target, source, uuid, version, **msg)


def decode_vex_message(frame):
    return decode(frame)


def create_request(source: str, type: str, version: str=VERSION, **request):
    source = source.encode('utf8')
    serialization = _json.dumps(('', type, version, request)).encode('utf8')
    return (source, serialization)


class Request:
    def __init__(self,
                 command: str='',
                 source: str='',
                 version: str=VERSION,
                 *args,
                 **kwargs):

        self.source = source
        self.command = command
        self.version = version
        self.args = args
        self.kwargs = kwargs


class VexTypes:
    command = 'CMD'
    response = 'RSP'
    message = 'MSG'
    # STAUS ?
