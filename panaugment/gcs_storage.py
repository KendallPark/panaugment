from typing import Text, Union, List

import tensorflow as tf
from . import storage

class GCSStorage(storage.Storage):

  def __init__(self, read_fn=None, write_fn=None):
    self._read_fn = read_fn or GCSStorage._default_read_fn
    self._write_fn = write_fn or GCSStorage._default_write_fn

  @classmethod
  def _default_read_fn(cls, f):
    f.read()

  @classmethod
  def _default_write_fn(cls, f, element):
    f.write(element)

  def list_files(self, file_pattern: Union[Text, List[Text]]):
    return tf.io.gfile.glob(file_pattern)

  def load(self, filename, binary=True):
    binary_flag = 'b' if binary else ''
    with tf.io.gfile.GFile(filename, f'r{binary_flag}') as f:
      return self._read_fn(f)

  def save(self, element, filename, binary=True):
    binary_flag = 'b' if binary else ''
    with tf.io.gfile.GFile(filename, f'w{binary_flag}') as f:
      self._write_fn(f, element)