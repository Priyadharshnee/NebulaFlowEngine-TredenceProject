from typing import Any, Callable, Dict

# Type alias for a tool function:
# it takes a mutable state dict and returns the same (or new) dict.
ToolFunc = Callable[[Dict[str, Any]], Dict[str, Any]]


class NebulaToolRegistry:
    """
    Simple in-memory registry for tools (node functions).
    Tools are just Python functions that accept and mutate a state dict.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, ToolFunc] = {}

    def register(self, name: str, func: ToolFunc) -> None:
        """Register a tool function under a given name."""
        self._tools[name] = func

    def get(self, name: str) -> ToolFunc:
        """Retrieve a tool function by name. Raises KeyError if not found."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered in NebulaTools.")
        return self._tools[name]

    def list_tools(self) -> Dict[str, ToolFunc]:
        """Return the internal tool mapping (for debugging)."""
        return dict(self._tools)


# Global singleton registry instance
nebula_tools = NebulaToolRegistry()
