import unittest

from panaugment import augmenter, distortion, storage
from . import distortion_test

# from IPython import embed

class MockStorage(storage.Storage):
  def __init__(self):
    self.load_called = []
    self.save_called = []
    self.list_files_called = []
    self._filenames = ['file1', 'file2', 'file3', 'file4']
    self.files = {}

  @property
  def filenames(self):
    return self._filenames

  def list_files(self, *args):
    self.list_files_called.append(args)
    return self.filenames

  def load(self, *args):
    self.load_called.append(args)
    return self.files.get(args[0], 8)

  def save(self, *args):
    self.save_called.append(args)
    self.files[args[1]] = args[0]

  def reset(self):
    self.load_called = []
    self.save_called = []
    self.list_files_called = []
    self.files = {}

def mock_augmenter():
  storage = MockStorage()
  distortions = [distortion_test.ADD_DIST, distortion_test.SUB_DIST,
                         distortion_test.MULT_DIST, distortion_test.DIV_DIST]
  return augmenter.Augmenter('', distortions, storage, cache='Add')

class Augmenter(unittest.TestCase):
  def setUp(self):
    self._aug = mock_augmenter()
    self._distortions = self._aug.distortions
    self._storage = self._aug.storage_obj

  def test_something(self):
    pass

if __name__ == '__main__':
  unittest.main()