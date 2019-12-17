import unittest
import tensorflow as tf
from panaugment import tf_utils
from . import augmenter_test

# from IPython import embed


class TFUtilsTest(unittest.TestCase):

  def setUp(self):
    self._augmenter = augmenter_test.mock_augmenter()

  def test_randaugment_dataset(self):
    dataset = tf_utils.randaugment_dataset(self._augmenter, 5, tf.int32)
    iterations = list(dataset)
    pass


if __name__ == '__main__':
  unittest.main()
