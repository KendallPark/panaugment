import unittest

import panaugment

from panaugment import distortion

def int_add_fn(example, magnitude):
  return example + magnitude

class DistortionTest(unittest.TestCase):
  def setUp(self):
    self._add_distortion = distortion.Distortion('Add', int_add_fn)

  def test_distort(self):
    self.assertEqual(self._add_distortion.distort(3, 3), 6)
