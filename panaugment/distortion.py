from typing import Any, Text, Callable

class Distortion(object):
  def __init__(self, name: Text, distort_fn: Callable[[Any, float], Any], ):
    self._name = name
    self._distort_fn = distort_fn

  @property
  def name(self):
    return self._name

  def distort(self, example: Any, magnitude: float) -> Any:
    return self._distort_fn(example, magnitude)
