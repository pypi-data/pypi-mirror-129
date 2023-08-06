from napari_plugin_engine import napari_hook_implementation

from .property_plotter import PropertyPlotter


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return (PropertyPlotter, {'area': 'bottom', 'name': 'Property Plotter'})
