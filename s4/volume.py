import uuid
from typing import NamedTuple


class TVolumeCreate(NamedTuple):
    name: str # 'myvolume'
    size: str # '1024M' or '1G'


class Volume:
    def __init__(self,):
        self.uuid = str(uuid.uuid4())
    def __str__(self):
        return f"Volume<{self.uuid}>"