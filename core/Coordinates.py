""" This module contains all Coordinates classes. Coordinates represent a 2D or 3D position in a grid as well as
offering useful features such as calculating euclidean and manhattan distances between two positions.
"""
import abc
import math


class Coordinates(object):
    """ General blueprint for a coordinate.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getCoordinates(self):
        """ Returns a tuple or triplet containing x, y and eventually z coordinates of the position.

        Returns:
            (int, int) OR (int, int, int): The numerical values of the coordinate.
        """
        pass

    @abc.abstractmethod
    def getEuclideanDistanceFromCoordinate(self, coordinate):
        """ Calculates the euclidean distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The euclidean distance.
        """
        pass

    @abc.abstractmethod
    def getManhattanDistanceFroomCoordinate(self, coordinate):
        """ Calculates the manhattan distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The manhattan distance.
        """
        pass

    @abc.abstractmethod
    def getMooreNeigh(self, grid):
        """ Returns the coordinates of all moore neighbours (radius 1) of the current coordinate. Also takes the grid
         we are using to ensure that all moore neighbours are in the grid. (Eg: Not producing a moore neighbour (5,5)
         for a grid of size (4,4).)

         Args:

             grid (Grid): The grid we are referring to.

         Returns:
             [Coordinates] : A list of coordinate objects referring to the moore neighbours.
        """
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        """ Checks if two coordinates refer to the same position.

        Args:
            other (Coordinates): Another coordinate

        Returns:

            bool: True if they reefer to the same position, false otherwise.
        """
        pass

    @abc.abstractmethod
    def __add__(self, other):
        """ Adds two coordinates.
         For example: (1,1)+(2,3) = (3,4)

         Args:
             other (Coordinates): The coordinate we want to add.

         Returns:

            coordinate (Coordinates): A new coordinate object referring to a position that is the sum of the
            previous two.
        """
        pass

    @abc.abstractmethod
    def __sub__(self, other):
        """ Subtracts two coordinates.
         For example: (3,4)-(1,2) = (2,2)

         Args:
             other (Coordinates): The coordinate we want to subtract.

         Returns:

            coordinate (Coordinates): A new coordinate object referring to a position that is the difference of the
            previous two.
        """
        pass

    @abc.abstractmethod
    def __mul__(self, other):
        """ Performs a DOT MULTIPLICATION between a scalar and the current coordinate.
         For example: 2*(1,2) = (2,4)

         Args:
             other (double): The scalar we want to multiply by.

         Returns:

             coordinate (Coordinates): A new coordiante referring to the position which is the result of multiplying
             all terms of the previous coordinate by the scalar.
        """
        pass

    @abc.abstractmethod
    def __rmul__(self, other):
        """ Identical to __mul__ but allows coord*scalar in addition to scalar*coord.
        """
        pass


class Coordinates3D(Coordinates):
    """Implementation of a 3D Coordinates class
    """
    def __add__(self, other):
        """ Adds two coordinates.
         For example: (1,1,1)+(2,3,4) = (3,4,5)

         Args:
             other (Coordinates3D): The coordinate we want to add.

         Returns:

            coordinate (Coordinates3D): A new coordinate object referring to a position that is the sum of the
            previous two.
        """

        if (isinstance(other, Coordinates3D)):
            otherCoords = other.getCoordinates()

            return Coordinates3D(int(self.x + otherCoords[0]), int(self.y + otherCoords[1]),
                                 int(self.z + otherCoords[2]))

    def __sub__(self, other):
        """ Subtracts two coordinates.
         For example: (3,4,5)-(1,2,3) = (2,2,3)

         Args:
             other (Coordinates3D): The coordinate we want to subtract.

         Returns:

            coordinate (Coordinates3D): A new coordinate object referring to a position that is the difference of the
            previous two.
        """

        if (isinstance(other, Coordinates3D)):
            otherCoords = other.getCoordinates()

            return Coordinates3D(int(self.x - otherCoords[0]), int(self.y - otherCoords[1]),
                                 int(self.z - otherCoords[2]))

    def __mul__(self, other):
        """ Performs a DOT MULTIPLICATION between a scalar and the current coordinate.
         For example: 2*(1,2,3) = (2,4,6)

         Args:
             other (double): The scalar we want to multiply by.

         Returns:

             coordinate (Coordinates3D): A new coordiante referring to the position which is the result of multiplying
             all terms of the previous coordinate by the scalar.
        """
        if (isinstance(other, int) or isinstance(other, float)):
            return Coordinates3D(other * self.x, other * self.y, other * self.z)

    __rmul__ = __mul__

    def __init__(self, x, y, z):
        """ Creates the coordinates object

         Args:
             x (int): The x-position.
             y (int): The y-position.
             z (int): The z-position.
        """
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        """ Checks if two coordinates refer to the same position.

        Args:
            other (Coordinates): Another coordinate

        Returns:

            bool: True if they reefer to the same position, false otherwise.
        """

        otherC = other.getCoordinates()
        return self.x == otherC[0] and self.y == otherC[1] and self.z == otherC[2]

    def getCoordinates(self):
        """ Returns triplet containing x, y and z coordinates of the position.

        Returns:
            (int, int, int): The numerical values of the coordinate.
        """
        return (self.x, self.y, self.z)

    def getEuclideanDistanceFromCoordinate(self, coordinate):
        """ Calculates the euclidean distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The euclidean distance.
        """
        otherCoords = coordinate.getCoordinates()
        otherX = otherCoords[0]
        otherY = otherCoords[1]
        otherZ = otherCoords[2]

        return math.sqrt((self.x - otherX) ** 2 + (self.y - otherY) ** 2 + (self.z - otherZ) ** 2)

    def getManhattanDistanceFroomCoordinate(self, coordinate):
        """ Calculates the manhattan distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The manhattan distance.
        """
        otherCoords = coordinate.getCoordinates()
        otherX = otherCoords[0]
        otherY = otherCoords[1]
        otherZ = otherCoords[2]

        return abs(self.x - otherX) + abs(self.y - otherY) + abs(self.z - otherZ)

    def inGrid(self, grid):
        """ Checks if the current coordinate is in a grid. (Ie: Not referring to a point lying outside the grid.)

         Args:
             grid (Grid): The grid we want to check against.

         Returns:
             bool: True if the point is in the grid, false otherwise.

        """

        x = self.x
        y = self.y
        z = self.z

        gridSize = grid.getSize()
        gx = gridSize[0]
        gy = gridSize[1]
        gz = gridSize[2]

        if (x >= 0 and x < gx and y >= 0 and y < gy and z >= 0 and z < gz):
            return self

        return None

    def getMooreNeigh(self, grid):
        """ Returns the coordinates of all moore neighbours (radius 1) of the current coordinate. Also takes the grid
         we are using to ensure that all moore neighbours are in the grid. (Eg: Not producing a moore neighbour (5,5,5)
         for a grid of size (4,4,4).)

         Args:

             grid (Grid): The grid we are referring to.

         Returns:
             [Coordinates] : A list of coordinate objects referring to the moore neighbours.
        """

        x = self.x
        y = self.y
        z = self.z

        neigh = [
            Coordinates3D(x + 1, y + 1, z + 1),
            Coordinates3D(x + 1, y + 1, z - 1),
            Coordinates3D(x + 1, y + 1, z),
            Coordinates3D(x + 1, y - 1, z + 1),
            Coordinates3D(x + 1, y - 1, z - 1),
            Coordinates3D(x + 1, y - 1, z),
            Coordinates3D(x + 1, y, z + 1),
            Coordinates3D(x + 1, y, z - 1),
            Coordinates3D(x + 1, y, z),
            Coordinates3D(x - 1, y - 1, z - 1),
            Coordinates3D(x - 1, y + 1, z - 1),
            Coordinates3D(x - 1, y + 1, z),
            Coordinates3D(x - 1, y - 1, z),
            Coordinates3D(x - 1, y - 1, z - 1),
            Coordinates3D(x - 1, y - 1, z),
            Coordinates3D(x - 1, y, z + 1),
            Coordinates3D(x - 1, y, z - 1),
            Coordinates3D(x - 1, y, z),
            Coordinates3D(x, y + 1, z + 1),
            Coordinates3D(x, y + 1, z - 1),
            Coordinates3D(x, y + 1, z),
            Coordinates3D(x, y - 1, z + 1),
            Coordinates3D(x, y - 1, z - 1),
            Coordinates3D(x, y - 1, z),
            Coordinates3D(z, y, z + 1),
            Coordinates3D(x, y, z - 1),
            Coordinates3D(x, y, z)

        ]

        gridSize = grid.getSize()
        xMax = gridSize[0]
        yMax = gridSize[1]
        zMax = gridSize[2]

        neigh = [c for c in neigh if c.x >= 0 and c.x < xMax and c.y >= 0 and c.y < yMax and c.z >= 0 and c.z < zMax]

        return neigh


class Coordinates2D(Coordinates):
    def __add__(self, other):
        """ Adds two coordinates.
         For example: (1,1)+(2,3) = (3,4)

         Args:
             other (Coordinates): The coordinate we want to add.

         Returns:

            coordinate (Coordinates): A new coordinate object referring to a position that is the sum of the
            previous two.
        """

        if (isinstance(other, Coordinates2D)):
            otherCoords = other.getCoordinates()

            return Coordinates2D(int(self.x + otherCoords[0]), int(self.y + otherCoords[1]))

    def __sub__(self, other):
        """ Subtracts two coordinates.
         For example: (3,4)-(1,2) = (2,2)

         Args:
             other (Coordinates): The coordinate we want to subtract.

         Returns:

            coordinate (Coordinates): A new coordinate object referring to a position that is the difference of the
            previous two.
        """

        if (isinstance(other, Coordinates2D)):
            otherCoords = other.getCoordinates()

            return Coordinates2D(int(self.x - otherCoords[0]), int(self.y - otherCoords[1]))

    def __mul__(self, other):
        """ Performs a DOT MULTIPLICATION between a scalar and the current coordinate.
         For example: 2*(1,2) = (2,4)

         Args:
             other (double): The scalar we want to multiply by.

         Returns:

             coordinate (Coordinates): A new coordiante referring to the position which is the result of multiplying
             all terms of the previous coordinate by the scalar.
        """
        if (isinstance(other, int) or isinstance(other, float)):
            return Coordinates2D(other * self.x, other * self.y)

    __rmul__ = __mul__

    def __init__(self, x, y, ):
        """ Creates the coordinates object.

         Args:
             x (int): The x-position.
             y (int): The y-position.
        """

        self.x = x
        self.y = y

    def inGrid(self, grid):
        """ Checks if the current coordinate is in a grid. (Ie: Not referring to a point lying outside the grid.)

         Args:
             grid (Grid): The grid we want to check against.

         Returns:
             bool: True if the point is in the grid, false otherwise.

        """

        x = self.x
        y = self.y

        gridSize = grid.getSize()
        gx = gridSize[0]
        gy = gridSize[1]

        if (x >= 0 and x < gx and y >= 0 and y < gy):
            return self

        return None

    def __eq__(self, other):
        """ Checks if two coordinates refer to the same position.

        Args:
            other (Coordinates): Another coordinate

        Returns:

            bool: True if they reefer to the same position, false otherwise.
        """
        otherC = other.getCoordinates()
        return (self.x == otherC[0]) & (self.y == otherC[1])

    def getCoordinates(self):
        """ Returns tuple containing x and y coordinates of the position.

        Returns:
            (int, int): The numerical values of the coordinate.
        """
        return (self.x, self.y)

    def getEuclideanDistanceFromCoordinate(self, coordinate):
        """ Calculates the euclidean distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The euclidean distance.
        """

        otherCoords = coordinate.getCoordinates()
        otherX = otherCoords[0]
        otherY = otherCoords[1]

        return math.sqrt((self.x - otherX) ** 2 + (self.y - otherY) ** 2)

    def getManhattanDistanceFroomCoordinate(self, coordinate):
        """ Calculates the manhattan distance between the current coordinate and another coordinate.

         Args:
             coordinate (Coordinates): The coordinate we want to calculate the distance to.

         Returns:
             double: The manhattan distance.
        """

        otherCoords = coordinate.getCoordinates()
        otherX = otherCoords[0]
        otherY = otherCoords[1]

        return abs(self.x - otherX) + abs(self.y - otherY)

    def getMooreNeigh(self, grid):
        """ Returns the coordinates of all moore neighbours (radius 1) of the current coordinate. Also takes the grid
         we are using to ensure that all moore neighbours are in the grid. (Eg: Not producing a moore neighbour (5,5,5)
         for a grid of size (4,4,4).)

         Args:

             grid (Grid): The grid we are referring to.

         Returns:
             [Coordinates] : A list of coordinate objects referring to the moore neighbours.
        """

        x = self.x
        y = self.y

        gridSize = grid.getSize()
        xMax = gridSize[0]
        yMax = gridSize[1]

        neigh = [
            Coordinates2D(x - 1, y),
            Coordinates2D(x - 1, y - 1),
            Coordinates2D(x - 1, y + 1),
            Coordinates2D(x + 1, y),
            Coordinates2D(x + 1, y - 1),
            Coordinates2D(x + 1, y + 1),
            Coordinates2D(x, y + 1),
            Coordinates2D(x, y - 1)
        ]

        neigh = [c for c in neigh if c.x >= 0 and c.x < xMax and c.y >= 0 and c.y < yMax]

        return neigh
