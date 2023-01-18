from io import BytesIO
from uuid import uuid4

from matplotlib.pyplot import figure
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from pandas import DataFrame

from .._models.options import Options
from .._utils.preprocessor import validate_dataframe
from .._utils.log import logger


def service(data: DataFrame, options: Options) -> bytes:
    """Triggers the plotter engine for the given request"""

    logger.debug("Preprocessing input data.")
    data = validate_dataframe(data)

    logger.debug("Building plot for given inputs.")
    plot = build_plot(data, options)

    return plot


def build_plot(data, options):
    uid = uuid4()
    fig: Figure = figure(uid)
    axes: Axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    xdata = data.index.values
    ydata = data[data.keys()[0]].values

    axes.plot(xdata, ydata, color=options.color)
    axes.scatter(xdata, ydata, color="red")
    set_configurations(axes, options)

    buf = BytesIO()
    fig.savefig(buf, format="png")

    return buf.getvalue()


def set_configurations(axes: Axes, configs: Options) -> None:
    axes.set_title(
        label=configs.title.label,
        color=configs.title.color,
        fontsize=configs.title.fontsize,
    )
    axes.set_xlabel(xlabel=configs.xlabel)
    axes.set_ylabel(ylabel=configs.ylabel)
