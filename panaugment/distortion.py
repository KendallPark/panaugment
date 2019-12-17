from typing import Any, Text, Callable, Union, NewType

import decimal

Magnitude = NewType('Magnitude', Union[int, float, decimal.Decimal, Text])

class Distortion(object):
  def __init__(self,
      name: Text,
      distort_fn: Callable[[Any, Magnitude], Any],
      default_magnitude: Magnitude = None):
    self._name = name
    self._distort_fn = distort_fn
    self._default_magnitude = None
    if default_magnitude is not None:
      self._default_magnitude = decimal.Decimal(default_magnitude)

  @property
  def name(self) -> Text:
    return self._name

  def distort(self, element: Any, magnitude: Magnitude) -> Any:
    return self._distort_fn(element, magnitude)

