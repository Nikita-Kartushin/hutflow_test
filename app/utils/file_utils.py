import os.path
from requests_toolbelt.multipart.encoder import MultipartEncoder


class FileUtils:
    @classmethod
    def get_candidates_resume(cls, candidate_name: str, position: str, path: str):
        _path = path.split('/')
        _path = _path[:-1]
        _path = '/'.join(_path)
        _path = os.path.join(_path, position)

        files = os.listdir(_path)
        for file in files:
            if candidate_name == next(iter(file.split('.'))):
                _path = os.path.join(_path, file)
                return open(_path, 'rb')
