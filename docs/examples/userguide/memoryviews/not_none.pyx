import numpy as np

def process_buffer(i32[:, :] input_view not None,
                   i32[:, :] output_view=None):
    if output_view is None:
        # Creating a default view, e.g.
        output_view = np.empty_like(input_view)

    # process 'input_view' into 'output_view'
    return output_view

process_buffer(None, None)
