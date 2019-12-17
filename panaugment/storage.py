from typing import Text, Any, List

class Storage(object):

  def __init__(self, list_files_fn, load_fn, save_fn):
    self._list_files_fn = list_files_fn
    self._load_fn = load_fn
    self._save_fn = save_fn

  def list_files(self, file_pattern) -> List[Text]:
    return self._list_files_fn(file_pattern)

  def load(self, filename: Text) -> Any:
    return self._load_fn(filename)

  def save(self, element: Any, filename: Text) -> Any:
    return self._save_fn(element, filename)