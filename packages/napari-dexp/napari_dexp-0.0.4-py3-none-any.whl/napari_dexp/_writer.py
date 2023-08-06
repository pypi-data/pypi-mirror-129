"""
This module is an example of a barebones writer plugin for napari

It implements the ``napari_get_writer`` and ``napari_write_image`` hook specifications.
see: https://napari.org/docs/dev/plugins/hook_specifications.html

Replace code below according to your needs
"""

from napari_plugin_engine import napari_hook_implementation
from typing import Callable, Optional, Any, Dict, List, Tuple
from dexp.datasets.zarr_dataset import ZDataset


SUPPORTED_TYPES = ['image', 'labels']


def is_valid_extension(path: str) -> bool:
    if path.endswith('.zarr') or path.endswith('.zarr.zip'):
        return True
    return False


@napari_hook_implementation
def napari_get_writer(path: str, layer_types: List[str]) -> Optional[Callable]:
    if not is_valid_extension(path):
        return None

    for layer_type in layer_types:
        if layer_type not in SUPPORTED_TYPES:
            return None

    return writer


def writer(path: str, layers_data: List[Tuple[Any, Dict, str]]) -> str:
    if not is_valid_extension(path):
        return None

    dataset = ZDataset(path, mode='w-')

    for data, meta, ltype in layers_data:
        dataset.add_channel(meta['name'],
                            shape=data.shape,
                            dtype=data.dtype)
        dataset.write_array(meta['name'], data)

    dataset.close()
    return path


@napari_hook_implementation
def napari_write_image(path: str, data: Any, meta: Dict) -> str:
    return writer(path, [(data, meta, 'image')])


@napari_hook_implementation
def napari_write_labels(path: str, data: Any, meta: Dict) -> str:
    return writer(path, [(data, meta, 'labels')])
