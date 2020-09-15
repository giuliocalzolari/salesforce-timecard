try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
_metadata = importlib_metadata.metadata(__name__)
__description__ = _metadata["Summary"]
