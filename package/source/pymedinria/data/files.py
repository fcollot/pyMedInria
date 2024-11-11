# Copyright (c) 2024 IHU Liryc, Université de Bordeaux, Inria.
# License: BSD-3-Clause


import hashlib
from threading import RLock
import weakref


_readers = []
_writers = []
_cache = {}
_lock = RLock()


def add_reader(self, reader):
    self._readers.append(reader)

    def add_writer(self, writer):
        self._writers.append(writer)

    def read(self, filepath):
        filehash = self._file_hash(filepath)
        with self._lock:
            try:
                return self._get_cache(filepath, filehash)
            except KeyError:
                for reader in self._readers:
                    try:
                        object = reader(filepath)
                    except:
                        pass
                    finally:
                        project = None#self._find_project(filepath) if not isinstance(object, Project) else object
                        self._add_cache(filepath, filehash, object, project)
                        return object, project
                raise RuntimeError('No suitable reader found')

    def write(self, object, filepath):
        with self._lock:
            for writer in self._writers:
                try:
                    writer(object, filepath)
                    filehash = self._file_hash(filepath)
                    self._add_cache(filepath, filehash, object, None) # project
                    return
                except:
                    pass
            raise RuntimeError('No suitable writer found')

    def _add_cache(self, filepath, filehash, object, project):
        self._cache[filepath] = {
            'hash': filehash,
            'object': weakref.ref(object, lambda _ : self._remove_cache(filepath)),
            'project': project,
        }

    def _get_cache(self, filepath, filehash):
        cache_entry = self._cache[filepath]
        if cache_entry['hash'] == filehash:
            return cache_entry['object'](), cache_entry['project']
        raise KeyError()

    def _remove_cache(self, filepath):
        del self._cache[filepath]

    def _find_project(self, filepath):
        project_file = self._find_project_file(filepath)
        if project_file:
            try:
                return self.read(project_file)
            except:
                pass
        return None

    def _find_project_file(self, filepath):
        for parent_path in Path(filepath).parents:
            project_file = parent_path.joinpath(Project.PROJECT_FILE_NAME)
            if project_file.exists() and project_file.is_file():
                return project_file
        return None

    def _file_hash(self, filepath):
        result = hashlib.sha1()
        with open(filepath,'rb') as file:
            while True:
                chunk = file.read(1024)
                if chunk != b'':
                    result.update(chunk)
                else:
                    return result.hexdigest()
