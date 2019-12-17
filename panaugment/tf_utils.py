import tensorflow as tf

from panaugment import augmenter, distortion

from typing import Callable, Any, List, Text

import numpy as np

# from IPython import embed


def randaugment(distortion_names: List[Text], depth: int,
    magnitude: distortion.Magnitude) -> List[augmenter.DistortionMagnitudePair]:
  sampled_ops = np.random.choice(distortion_names, depth)
  return [(op, magnitude) for op in sampled_ops]


def randaugment_dataset(
    aug: augmenter.Augmenter,
    global_magnitude: distortion.Magnitude,
    output_types: Any,
    depth: int = 1,
    map_tf_fn: Callable[[Any], Any] = None,
    output_shapes: Any = None,
    args: Any = None):
  def map_tf(x):
    return x

  map_tf = map_tf_fn or map_tf

  def generator_fn():
    aug.update_cache_filenames()

    for filename in aug.filenames:
      element = aug.augment(filename, randaugment(aug.distortion_names, depth,
                                                  global_magnitude))
      yield map_tf(element)

  return tf.data.Dataset.from_generator(generator_fn, output_types, output_shapes, args)
