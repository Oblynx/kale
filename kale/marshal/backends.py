#  Copyright 2019-2020 The Kale Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import dill

from .resource_load import resource_load
from .resource_save import resource_save
from .resource_load import resource_all as fallback_load
from .resource_save import resource_all as fallback_save


# TODO: Add more backends for common data types


def _get_obj_name(s):
    return s.split('/')[-1]


@resource_load.register(r'.*\.npy')  # match anything ending in .npy
def resource_numpy_load(uri, **kwargs):
    """Load a numpy resource."""
    try:
        import numpy as np
        print("Loading numpy obj: {}".format(_get_obj_name(uri)))
        return np.load(uri)
    except ImportError:
        return fallback_load(uri, **kwargs)


@resource_save.register(r'numpy\..*')
def resource_numpy_save(obj, path, **kwargs):
    """Save a numpy resource."""
    try:
        import numpy as np
        print("Saving numpy obj: {}".format(_get_obj_name(path)))
        np.save(path + ".npy", obj)
    except ImportError:
        fallback_save(obj, path, **kwargs)


@resource_load.register(r'.*\.pdpkl')
def resource_pandas_load(uri, **kwargs):
    """Load a pandas resource."""
    try:
        import pandas as pd
        print("Loading pandas obj: {}".format(_get_obj_name(uri)))
        return pd.read_pickle(uri)
    except ImportError:
        return fallback_load(uri, **kwargs)


@resource_save.register(r'pandas\..*')
def resource_pandas_save(obj, path, **kwargs):
    """Save a pandas resource."""
    try:
        import pandas as pd  # noqa: F401
        print("Saving pandas obj: {}".format(_get_obj_name(path)))
        obj.to_pickle(path + '.pdpkl')
    except ImportError:
        fallback_save(obj, path, **kwargs)


@resource_load.register(r'.*\.pt')
def resource_torch_load(uri, **kwargs):
    """Load a torch resource."""
    try:
        import torch
        print("Loading PyTorch model: {}".format(_get_obj_name(uri)))
        obj_torch = torch.load(uri, pickle_module=dill)
        if "nn.Module" in str(type(obj_torch)):
            # if the object is a Module we need to run eval
            obj_torch.eval()
        return obj_torch
    except ImportError:
        return fallback_load(uri, **kwargs)


@resource_save.register(r'torch.*')
def resource_torch_save(obj, path, **kwargs):
    """Save a torch resource."""
    try:
        import torch
        print("Saving PyTorch model: {}".format(_get_obj_name(path)))
        torch.save(obj, path + ".pt", pickle_module=dill)
    except ImportError:
        fallback_save(obj, path, **kwargs)


@resource_load.register(r'.*\.keras')
def resource_keras_load(uri, **kwargs):
    """Load a Keras model."""
    try:
        from keras.models import load_model
        print("Loading Keras model: {}".format(_get_obj_name(uri)))
        obj_keras = load_model(uri)
        return obj_keras
    except ImportError:
        return fallback_load(uri, **kwargs)


@resource_save.register(r'keras.*')
def resource_keras_save(obj, path, **kwargs):
    """Save a Keras model."""
    try:
        print("Saving Keras model: {}".format(_get_obj_name(path)))
        obj.save(path + ".keras")
    except ImportError:
        fallback_save(obj, path, **kwargs)
