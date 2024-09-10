from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDatabase(ABC):
    @abstractmethod
    def create(self, table_name: str, item: Dict[str, Any]) -> None:
        """Create a new item in the specified table."""
        pass

    @abstractmethod
    def update(self, table_name: str, key: Dict[str, Any], update_expression: str, expression_values: Dict[str, Any]) -> None:
        """Update an existing item in the specified table."""
        pass

    @abstractmethod
    def select(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        """Select an item from the specified table."""
        pass
