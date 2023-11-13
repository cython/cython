import numpy as np
import typing

def process_buffer(input_view: cython.int[:,:],
                   output_view: typing.Optional[cython.int[:,:]] = None):

    if output_view is None:
        # Creating a default view, e.g.
        output_view = np.empty_like(input_view)

    # process 'input_view' into 'output_view'
    return output_view

process_buffer(None, None)
