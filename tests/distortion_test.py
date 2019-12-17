import unittest

from panaugment import distortion


def int_add_fn(example, magnitude):
  return example + magnitude


def int_sub_fn(example, magnitude):
  return example - magnitude


def int_mult_fn(example, magnitude):
  return example * magnitude


def int_div_fn(example, magnitude):
  return example / magnitude


ADD_DIST = distortion.Distortion('Add', int_add_fn)
SUB_DIST = distortion.Distortion('Sub', int_sub_fn)
MULT_DIST = distortion.Distortion('Mult', int_mult_fn)
DIV_DIST = distortion.Distortion('Div', int_div_fn)


class DistortionTest(unittest.TestCase):
  def setUp(self):
    self._add_distortion = distortion.Distortion('Add', int_add_fn)

  def test_distort(self):
    self.assertEqual(self._add_distortion.distort(3, 3), 6)


if __name__ == '__main__':
  unittest.main()
