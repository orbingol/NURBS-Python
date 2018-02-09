"""
.. module:: Multi
    :platform: Unix, Windows
    :synopsis: Container module for storage and visualization of curves and surfaces

.. moduleauthor:: Onur Rauf Bingol <orbingol@gmail.com>

"""

import abc
import random
import warnings

from . import Abstract
from geomdl.visualization import VisBase


# Generate random colors for plotting
def color_generator():
    """ Generate random colors for control and evaluated points plotting.

    Inspired from https://stackoverflow.com/a/14019260

    :return: list of color strings in hex format
    :rtype: list
    """
    r = lambda: random.randint(0, 255)
    color_string = '#%02X%02X%02X'
    return [color_string % (r(), r(), r()), color_string % (r(), r(), r())]


class MultiAbstract(object):
    """ Abstract class for curve and surface containers. """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._elements = []
        self._delta = 0.1
        self._vis_component = None
        self._iter_index = 0
        self._instance = None

    def __iter__(self):
        self._iter_index = 0
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            result = self._elements[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __reversed__(self):
        return reversed(self._elements)

    def __getitem__(self, index):
        return self._elements[index]

    def __len__(self):
        return len(self._elements)

    @property
    def delta(self):
        """ Evaluation delta.

        :getter: Gets the delta value
        :setter: Sets the delta value
        :type: float
        """
        return self._delta

    @delta.setter
    def delta(self, value):
        # Delta value for surface evaluation should be between 0 and 1
        if float(value) <= 0 or float(value) >= 1:
            raise ValueError("Surface evaluation delta should be between 0.0 and 1.0")

        # Set a new delta value
        self._delta = float(value)

    @property
    def vis(self):
        """ Visualization component.

        :getter: Gets the visualization component
        :setter: Sets the visualization component
        :type: float
        """
        return self._vis_component

    @vis.setter
    def vis(self, value):
        if not isinstance(value, VisBase.VisAbstract):
            warnings.warn("Visualization component is NOT an instance of the abstract class")
            return
        self._vis_component = value

    def add(self, element):
        """ Abstract method for adding surface or curve objects to the container.

        :param element: the curve or surface object to be added
        :type element:
        """
        if not isinstance(element, self._instance):
            warnings.warn("Cannot add, incompatible type.")
            return
        self._elements.append(element)

    def add_list(self, elements):
        """ Adds curve objects to the container.

        :param elements: curve objects to be added
        :type elements: list, tuple
        """
        if not isinstance(elements, (list, tuple)):
            warnings.warn("Input must be a list or a tuple")
            return

        for element in elements:
            self.add(element)

    # Runs visualization component to render the surface
    @abc.abstractmethod
    def render(self):
        """ Abstract method for rendering plots using the visualization component. """
        pass


class MultiCurve(MultiAbstract):
    """ Container class for storing multiple curves.

    The elements contained in this class can be 2D or 3D curves but there are no checks for the curve types.

    Visualization depends on the visualization instance, e.g. you can visualize a 3D curve using a ``VisCurve2D``
    instance but you cannot visualize a 2D curve with a ``VisCurve3D`` instance.
    """

    def __init__(self):
        super(MultiCurve, self).__init__()
        self._instance = Abstract.Curve

    def render(self):
        """ Renders the curve the using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has set")
            return

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            elem.delta = self._delta
            elem.evaluate()
            color = color_generator()
            self._vis_component.add(ptsarr=elem.ctrlpts,
                                    name="Control Points " + str(idx + 1),
                                    color=color[0],
                                    plot_type=1)
            self._vis_component.add(ptsarr=elem.curvepts,
                                    name="Curve " + str(idx + 1),
                                    color=color[1])
        self._vis_component.render()


class MultiSurface(MultiAbstract):
    """ Container class for storing multiple surfaces. """

    def __init__(self):
        super(MultiSurface, self).__init__()
        self._instance = Abstract.Surface

    def render(self):
        """ Renders the surface the using the visualization component.

        The visualization component must be set using :py:attr:`~vis` property before calling this method.
        """
        if not self._vis_component:
            warnings.warn("No visualization component has set")
            return

        # Run the visualization component
        self._vis_component.clear()
        for idx, elem in enumerate(self._elements):
            elem.delta = self._delta
            elem.evaluate()
            color = color_generator()
            self._vis_component.add(ptsarr=elem.ctrlpts,
                                    size=[elem.ctrlpts_size_u, elem.ctrlpts_size_v],
                                    name="Control Points " + str(idx + 1),
                                    color=color[0],
                                    plot_type=1)
            self._vis_component.add(ptsarr=elem.surfpts,
                                    size=[int((1.0 / self._delta) + 1), int((1.0 / self._delta) + 1)],
                                    name="Surface " + str(idx + 1),
                                    color=color[1])
        self._vis_component.render()
