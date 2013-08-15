from uuid import uuid4
from hashlib import md5
from inspect import getmembers, ismethod
from collections import defaultdict, deque, Counter


class IndexEntry(object):
    '''Class the inspects a dictionary and yields tuples of
    values and keypaths for creating an index.
    '''
    def __init__(self, obj):
        self.obj = obj

    def _handle_value(self, value, pathsegs=None):
        pathsegs = list(pathsegs or [])
        if isinstance(value, dict):
            yield from self._generate_obj_items(value, pathsegs)
        elif isinstance(value, (list, tuple, set)):
            yield from self._generate_list_items(value, pathsegs)
        else:
            yield ('.'.join(pathsegs), value)

    def _generate_obj_items(self, obj, pathsegs=None):
        pathsegs = list(pathsegs or [])
        for key, value in obj.items():
            _pathsegs = pathsegs[:]
            _pathsegs.append(key)
            yield from self._handle_value(value, _pathsegs)

    def _generate_list_items(self, obj, pathsegs=None):
        pathsegs = list(pathsegs or [])
        for key, value in enumerate(obj):
            _pathsegs = pathsegs[:]
            _pathsegs.append(str(key))
            yield from self._handle_value(value, _pathsegs)

    def __iter__(self):
        yield from self._handle_value(self.obj)


class _IndexMaps(object):
    '''Helper to hold the index dictionaries.
    '''
    def __init__(self):
        self.keypath_value_id = defaultdict(lambda: defaultdict(list))
        self.value_id_keypath = defaultdict(lambda: defaultdict(list))
        self.values = {}


class Index(object):
    '''Main index object and helper methods.
    '''
    def __init__(self):
        self.maps = _IndexMaps()

    def _add_item(self, object_id, keypath, value):
        value_id = md5(str(value).encode('utf-8')).hexdigest()

        # Maps [keypath][value_id] to a list of object ids.
        self.maps.keypath_value_id[keypath][value_id].append(object_id)

        # Maps [value_id][object_id] to a list of keypaths.
        self.maps.value_id_keypath[value_id][object_id].append(keypath)

        # Map value_id to its value.
        self.maps.values[value_id] = value

    def add_object(self, obj, object_id=None):
        if object_id is None:
            object_id = str(uuid4())
        for item in IndexEntry(obj):
            self._add_item(object_id, *item)

    def show_keys(self):
        for key, val in self.maps.keypath_value_id.items():
            print(key, len(val))

    def keypaths_for_value(self, value, object_id=None):
        '''Given a value, retrieve all dict of object_ids, each mapping
        to a list of keypaths that end in that value.
        '''
        value_id = md5(str(value).encode('utf-8')).hexdigest()
        res = self.maps.value_id_keypath[value_id]
        if object_id is None:
            return dict(res)
        else:
            return res[object_id]
