try:
    from ipywidgets import interact
    import ipywidgets as widgets
    import matplotlib.pyplot as plt
except ImportError:
    ipywidgets = None

import numpy as np

from openmdao.recorders.case_reader import CaseReader
from openmdao.utils.general_utils import simple_warning


class CasesWidget(object):
    """
    Widget to plot s variable over a sequence of cases.

    Parameters
    ----------
    cr : CaseReader or str
        CaseReader or path to the recorded data file.
    """

    def __init__(self, cr):
        """
        Initialize.
        """
        if ipywidgets is None:
            simple_warning("ipywidgets is not installed. Run `pip install openmdao[notebooks]`.")
            return

        if isinstance(cr, str):
            cr = CaseReader(cr)

        w_source = widgets.Dropdown(
            options=cr.list_sources(out_stream=None),
            description='Source:',
            disabled=False,
        )

        w_cases = widgets.IntRangeSlider(
            value=[0, len(cr.list_cases(w_source.value, out_stream=None))-1],
            min=0,
            max=len(cr.list_cases(w_source.value, out_stream=None))-1,
            step=1,
            description='Cases',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
        )

        def update_cases_range(*args):
            last_case = len(cr.list_cases(w_source.value, out_stream=None))-1
            w_cases.max = last_case
            w_cases.value=[0, last_case]
        w_source.observe(update_cases_range, 'value')

        w_outvar = widgets.Dropdown(
            options=cr.list_source_vars(w_source.value, out_stream=None)['outputs'],
            description='Output:',
            disabled=False,
        )

        def plot_func(source, cases, outvar):
            case_ids = cr.list_cases(source, out_stream=None)
            case_nums = np.arange(cases[0], cases[1]+1, dtype=int)
            selected = [case_ids[n] for n in case_nums]
            vals = [cr.get_case(case_id).outputs[outvar] for case_id in selected]
            y = np.array(vals)
            plt.grid(True)
            plt.xticks(case_nums)
            plt.plot(case_nums, y)

        interact(plot_func, source=w_source, cases=w_cases, outvar=w_outvar, description=f"cases for {w_source.value}", disabled=False)
