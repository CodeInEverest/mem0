#import importlib.metadata

#__version__ = importlib.metadata.version("mem0ai")
__version__ = "1.0.0"
from mem0.memory.main import Memory  # noqa
from mem0.client.main import MemoryClient  # noqa
