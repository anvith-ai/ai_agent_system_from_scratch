from typing import List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MemoryItem:
    """Represents a single memory item in the agent's memory."""
    content: str
    timestamp: datetime
    source: str  # 'user' or 'agent'
    
class Memory:
    """Manages the agent's memory system."""
    
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self._memory: List[MemoryItem] = []
    
    def add(self, content: str, source: str):
        """Add a new item to memory."""
        item = MemoryItem(
            content=content,
            timestamp=datetime.now(),
            source=source
        )
        self._memory.append(item)
        self._memory = self._memory[-self.max_items:]
    
    def get_context(self) -> str:
        """Get formatted context from memory items."""
        return "\n".join([
            f"{item.source.capitalize()}: {item.content}"
            for item in self._memory
        ])