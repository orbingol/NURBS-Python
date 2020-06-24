"""
.. module:: containers
    :platform: Unix, Windows
    :synopsis: Provides container classes for geometry objects

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from six import add_metaclass
from .base import export, GeomdlError, GeomdlTypeSequence
from .abstract import Geometry
from . import utilities


@export
class GeometryContainer(Geometry):
    """ Abstract class for geometry containers """
    def __init__(self, *args, **kwargs):
        cache_vars = kwargs.get('cache_vars', dict())
        cache_vars.update(dict(evalpts=list()))
        kwargs.update(dict(cache_vars=cache_vars))
        super(GeometryContainer, self).__init__(*args, **kwargs)
        self._geometry_type = "container"
        self._geoms = []
        for arg in args:
            self.add(arg)

    def __next__(self):
        try:
            result = self._geoms[self._iter_index]
        except IndexError:
            raise StopIteration
        self._iter_index += 1
        return result

    def __reversed__(self):
        return reversed(self._geoms)

    def __getitem__(self, index):
        return self._geoms[index]

    def __len__(self):
        return len(self._geoms)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise GeomdlError("Cannot add non-matching container types")
        self.add(other)
        return self

    @property
    def evalpts(self):
        """ Evaluated points

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.

        :getter: Gets the evaluated points of all contained geometries
        """
        if not self._cache['evalpts']:
            for g in self._geoms:
                self._cache['evalpts'] += g.evalpts
        return self._cache['evalpts']

    @property
    def data(self):
        """ Returns a dict which contains the geometry data.

        Please refer to the `wiki <https://github.com/orbingol/NURBS-Python/wiki/Using-Python-Properties>`_ for details
        on using this class member.
        """
        return tuple([g.data for g in self._geoms])

    def add(self, geom):
        """ Adds geometry objects to the container.

        The input can be a single geometry, a list of geometry objects or a geometry container object.

        :param element: geometry object
        """
        if isinstance(geom, (self.__class__, GeomdlTypeSequence)):
            for g in geom:
                self.add(g)
        elif isinstance(geom, Geometry):
            self._geoms.append(geom)
        else:
            raise GeomdlError("Cannot add the element to the container")

        # Reset the cache
        self.reset()

    # Make container look like a list
    append = add
