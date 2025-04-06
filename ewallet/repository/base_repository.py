import abc
from typing import Any, Optional

class BaseRepository(abc.ABC):

  @abc.abstractmethod
  def save(self, entity) -> str:
    """
    Saves entity to the repository.

    :param entity: entity to save
    :return: id of the saved entity
    """
    pass

  @abc.abstractmethod
  def find(self, id) -> Optional[Any]:
    """
    Finds entity by id.

    :param id: id of the entity
    :return: the entity or None if not found
    """
    pass
