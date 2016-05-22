""" A general module aimed at providing a blueprint for grid graphic displayers.
"""

import abc
import Tkinter
from time import *
from panacea.core.Coordinates import *
from panacea.core.Grid import ObjectGrid2D
from panacea.core.Steppables import *
from panacea.examples.gameOfLife.GameOfLife import *


class GridDisplayHelper(Helper):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def renderGrid(self, grid):
        """ Blueprint for the renderGrid method.

         Args:

             grid (Grid): The grid we are rendering.
        """
        pass


