from typing import Text, Union, List

import tensorflow as tf
from . import storage

class GCSStorage(storage.Storage):

  def __init__(self):
    super().__init__(GCSStorage._list_files_fn, GCSStorage._load_fn, GCSStorage._save_fn)

  @classmethod
  def _list_files_fn(cls, file_pattern: Union[Text, List[Text]]):
    tf.io.gfile.glob(file_pattern)

  @classmethod
  def _load_fn(cls, filename, binary=False):
    binary_flag = 'b' if binary else ''
    with tf.io.gfile.GFile(filename, f'r{binary_flag}') as f:
      return f.read()

  @classmethod
  def _save_fn(cls, element, filename, binary=False):
    binary_flag = 'b' if binary else ''
    with tf.io.gfile.GFile(filename, f'w{binary_flag}') as f:
      f.write(element)