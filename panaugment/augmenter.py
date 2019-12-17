from typing import Text, List, Callable, Union, Any, Tuple, NewType

from . import distortion
from . import storage

import decimal
import os

import hashlib

# from IPython import embed

DistortionMagnitudePair = NewType('DistortionMagnitudePair',
                                  Tuple[Text, distortion.Magnitude])

class Augmenter(object):
  def __init__(self,
      file_pattern: Union[Text, List[Text]],
      distortions: List[distortion.Distortion],
      storage_obj: storage.Storage,
      deserialize_fn: Callable[[Any], Any] = None,
      cache_serialize_fn: Callable[[Any], Any] = None,
      cache_deserialize_fn: Callable[[Any], Any] = None,
      cache: Union[Text, List[Text]] = None,
      cache_dir: Text = 'cache/',
      cache_depth: int = 1,
      cache_storage_obj: storage.Storage = None,
      cache_map_fn: Callable[[Text], Any] = None,
      magnitude_str_fn: Callable[[distortion.Magnitude], Text] = None):

    self._storage_obj = storage_obj
    self._cache_storage_obj = cache_storage_obj or storage_obj
    self._source_files = storage_obj.list_files(file_pattern)
    self._distortions = distortions
    self._distortions_by_name = {d.name: d for d in distortions}

    if cache is None:
      self._cache = set([])
    elif isinstance(cache, str):
      self._cache = set([cache])
    else:
      self._cache = set(cache)
    self._cache_dir = cache_dir
    self._cache_depth = cache_depth

    def identity(x):
      return x
    self._deserialize_fn = deserialize_fn or identity
    self._cache_serialize_fn = cache_serialize_fn or identity
    self._cache_deserialize_fn = cache_deserialize_fn or identity

    def default_magnitude_str_fn(magnitude):
      if isinstance(magnitude, str):
        return magnitude
      m = decimal.Decimal(magnitude)
      if isinstance(magnitude, float):
        return str(f'{m:.4f}')
      return str(m)

    self._magnitude_str_fn = magnitude_str_fn or default_magnitude_str_fn

    self._cache_filenames = set()
    self.update_cache_filenames()

    self._cache_map_fn = cache_map_fn or identity

  @property
  def filenames(self) -> List[Text]:
    return self._source_files

  @property
  def distortions(self) -> List[distortion.Distortion]:
    return self._distortions

  @property
  def distortion_names(self) -> List[Text]:
    return list(self._distortions_by_name.keys())

  @property
  def storage_obj(self) -> storage.Storage:
    return self._storage_obj

  @property
  def cache_storage_obj(self) -> storage.Storage:
    return self._cache_storage_obj

  def _cache_filename(self, filename):
    return filename.replace('://', '.').replace('/', '.')

  def cache_path(self, filename: Text,
      distortion_steps: List[Tuple[Text, distortion.Magnitude]]) -> Text:
    name = self._cache_filename(filename)
    dmlist = [(dm[0], self._magnitude_str_fn(dm[1])) for dm in distortion_steps]
    path = os.path.join(self._cache_dir, name,
                        *[str(item) for dmpair in dmlist for item in dmpair])
    return f'{path}.cache'

  def cache_paths(self, filename: Text,
      distortion_steps: List[Tuple[Text, distortion.Magnitude]]) -> List[Text]:
    return [self.cache_path(filename, distortion_steps[0:i + 1]) for i in
            range(len(distortion_steps))]

  def fetch_cache_filenames(self) -> List[Text]:
    file_patterns = self.cache_paths('*', [('*', '*') for i in
                                           range(self._cache_depth)])
    return self._cache_storage_obj.list_files(file_patterns) or []

  def update_cache_filenames(self) -> None:
    self._cache_filenames = set(self.fetch_cache_filenames())

  def augment(self, filename: Text, distortion_steps: Union[
    DistortionMagnitudePair, List[DistortionMagnitudePair]]) -> Any:
    dmlist = distortion_steps
    if not isinstance(dmlist, list):
      dmlist = [distortion_steps]
    paths = self.cache_paths(filename, dmlist)

    element = None

    remainder = []
    dmlist = distortion_steps.copy()
    while len(dmlist) > 0:
      path = self.cache_path(filename, dmlist)
      if path in self._cache_filenames:
        element = self._cache_deserialize_fn(self._cache_storage_obj.load(path))
        break
      remainder.insert(0, dmlist.pop())

    if element is None:
      element = self._deserialize_fn(self._storage_obj.load(filename))

    for i in range(len(remainder)):
      distortion_name, magnitude = remainder[i]
      element = self.apply_distortion(element, distortion_name, magnitude)
      if i < self._cache_depth and distortion_name in self._cache:
        path = self.cache_path(filename, remainder[0:i + 1])
        self._cache_storage_obj.save(self._cache_serialize_fn(element), path)
        self._cache_filenames.add(path)

    return self._cache_map_fn(element)

  def apply_distortion(self, element: Any, distortion_name: Text,
      magnitude: distortion.Magnitude) -> Any:
    return self._distortions_by_name[distortion_name].distort(element,
                                                              magnitude)
