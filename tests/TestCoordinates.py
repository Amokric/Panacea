import unittest

from panacea.core.Coordinates import *
from panacea.core.Grid import ObjectGrid2D, ObjectGrid3D


class TestCoordinates(unittest.TestCase):
    def test_coordinate_2d_setup(self):
        c = Coordinates2D(1, 2)

        coordinates = c.getCoordinates()
        self.assertEqual(1, coordinates[0])
        self.assertEqual(2, coordinates[1])

    def test_coordinate_2d_euclidean_distance(self):
        cA = Coordinates2D(1, 1)
        cB = Coordinates2D(2, 2)

        self.assertEqual(math.sqrt(2), cA.getEuclideanDistanceFromCoordinate(cB))
        self.assertEqual(math.sqrt(2), cB.getEuclideanDistanceFromCoordinate(cA))

    def test_coordinate_2d_manhattan_distance(self):
        cA = Coordinates2D(1, 1)
        cB = Coordinates2D(2, 2)

        self.assertEqual(2, cA.getManhattanDistanceFroomCoordinate(cB))
        self.assertEqual(2, cB.getManhattanDistanceFroomCoordinate(cA))

    def test_coordinate_2d_eq(self):
        x = Coordinates2D(1, 1)
        y = Coordinates2D(1, 1)

        self.assertEqual(x, y)

        x = Coordinates2D(1, 2)
        y = Coordinates2D(2, 2)

        self.assertNotEqual(x, y)

    def test_coordinate_2d_get_moore_neigh(self):
        grid = ObjectGrid2D(5, 5, "")

        c = Coordinates2D(2, 2)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(1, 2),
            Coordinates2D(1, 1),
            Coordinates2D(1, 3),
            Coordinates2D(3, 2),
            Coordinates2D(3, 1),
            Coordinates2D(3, 3),
            Coordinates2D(2, 3),
            Coordinates2D(2, 1)
        ]

        self.assertEqual(expNeigh, neigh)

        # And..... now we test borderline cases, FUN!


        # Corner 1 (bottom-left)
        c = Coordinates2D(0, 0)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(1, 0),
            Coordinates2D(1, 1),
            Coordinates2D(0, 1)
        ]

        self.assertEqual(expNeigh, neigh)

        # Edge 1 (left)
        c = Coordinates2D(0, 1)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(1, 1),
            Coordinates2D(1, 0),
            Coordinates2D(1, 2),
            Coordinates2D(0, 2),
            Coordinates2D(0, 0)
        ]

        self.assertEqual(expNeigh, neigh)

        # Corner 2 (top-left)
        c = Coordinates2D(0, 4)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(1, 4),
            Coordinates2D(1, 3),
            Coordinates2D(0, 3)
        ]

        self.assertEqual(expNeigh, neigh)

        # Edge 2 (top)
        c = Coordinates2D(1, 4)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(0, 4),
            Coordinates2D(0, 3),
            Coordinates2D(2, 4),
            Coordinates2D(2, 3),
            Coordinates2D(1, 3)
        ]

        self.assertEqual(expNeigh, neigh)

        # Corner 3 (top-right)

        c = Coordinates2D(4, 4)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(3, 4),
            Coordinates2D(3, 3),
            Coordinates2D(4, 3)
        ]

        self.assertEqual(expNeigh, neigh)

        # Edge 3 (Right)


        c = Coordinates2D(4, 2)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(3, 2),
            Coordinates2D(3, 1),
            Coordinates2D(3, 3),
            Coordinates2D(4, 3),
            Coordinates2D(4, 1),
        ]

        self.assertEqual(expNeigh, neigh)

        # Corner 4 (bottom right)

        c = Coordinates2D(4, 0)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(3, 0),
            Coordinates2D(3, 1),
            Coordinates2D(4, 1)
        ]

        self.assertEqual(expNeigh, neigh)

        # Edge 4 (bottom)

        c = Coordinates2D(1, 0)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
            Coordinates2D(0, 0),
            Coordinates2D(0, 1),
            Coordinates2D(2, 0),
            Coordinates2D(2, 1),
            Coordinates2D(1, 1)
        ]

        self.assertEqual(expNeigh, neigh)

    def test_coordinate_3d_setup(self):
        c = Coordinates3D(1, 2, 3)

        coordinates = c.getCoordinates()
        self.assertEqual(1, coordinates[0])
        self.assertEqual(2, coordinates[1])
        self.assertEqual(3, coordinates[2])

    def test_coordinate_3d_euclidean_distance(self):
        cA = Coordinates3D(1, 1, 1)
        cB = Coordinates3D(2, 2, 2)

        self.assertEqual(math.sqrt(3), cA.getEuclideanDistanceFromCoordinate(cB))
        self.assertEqual(math.sqrt(3), cB.getEuclideanDistanceFromCoordinate(cA))

    def test_coordinate_3d_manhattan_distance(self):
        cA = Coordinates3D(1, 1, 1)
        cB = Coordinates3D(2, 2, 2)

        self.assertEqual(3, cA.getManhattanDistanceFroomCoordinate(cB))
        self.assertEqual(3, cB.getManhattanDistanceFroomCoordinate(cA))

    def test_add(self):
        a = Coordinates2D(1, 1)
        b = Coordinates2D(3, 3)

        self.assertEqual(Coordinates2D(4, 4), a + b)

    def test_subtract(self):
        a = Coordinates2D(3, 3)
        b = Coordinates2D(1, 1)

        self.assertEqual(Coordinates2D(2, 2), a - b)

    def test_scalar_mult(self):
        a = Coordinates2D(1, 1)

        self.assertEqual(Coordinates2D(2, 2), 2 * a)

    def test_eq_coord_3d(self):
        a = Coordinates3D(1, 1, 1)
        b = Coordinates3D(1, 1, 1)
        c = Coordinates3D(1, 1, 2)

        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_add_coord_3d(self):
        a = Coordinates3D(1, 2, 3)
        b = Coordinates3D(4, 5, 6)

        self.assertEqual(Coordinates3D(5, 7, 9), a + b)

    def test_sub_coord_3d(self):
        a = Coordinates3D(4, 5, 6)
        b = Coordinates3D(1, 2, 3)

        self.assertEqual(Coordinates3D(3, 3, 3), a - b)

    def test_scalar_mul_coord_3d(self):
        a = Coordinates3D(1, 1, 1)
        self.assertEqual(Coordinates3D(2, 2, 2), 2 * a)
        self.assertEqual(Coordinates3D(2, 2, 2), a * 2)

    def test_coordinate_in_grid_2d(self):
        grid = ObjectGrid2D(15, 15, "")

        cA = Coordinates2D(2, 2)
        self.assertEqual(cA, cA.inGrid(grid))

        cB = Coordinates2D(-1, 2)
        self.assertEqual(None, cB.inGrid(grid))

        cC = Coordinates2D(1, -2)
        self.assertEqual(None, cC.inGrid(grid))

        cD = Coordinates2D(1, 17)

        self.assertEqual(None, cD.inGrid(grid))

        cE = Coordinates2D(17, 1)
        self.assertEqual(None, cE.inGrid(grid))

        cF = Coordinates2D(14, 14)
        self.assertEqual(cF, cF.inGrid(grid))

    def test_coordinate_in_grid_3d(self):
        grid = ObjectGrid3D(15, 15, 15, "")

        cA = Coordinates3D(1, 1, 1)
        self.assertEqual(cA, cA.inGrid(grid))

        cB = Coordinates3D(-1, 1, 1)
        self.assertEqual(None, cB.inGrid(grid))

        cB = Coordinates3D(1, -1, 1)
        self.assertEqual(None, cB.inGrid(grid))

        cB = Coordinates3D(1, 1, -1)
        self.assertEqual(None, cB.inGrid(grid))

        cC = Coordinates3D(15, 1, 1)
        self.assertEqual(None, cC.inGrid(grid))

        cC = Coordinates3D(1, 15, 1)
        self.assertEqual(None, cC.inGrid(grid))

        cC = Coordinates3D(1, 1, 15)
        self.assertEqual(None, cC.inGrid(grid))

    def test_coordinate_3d_get_moore_neigh(self):
        grid = ObjectGrid3D(15, 15, 15, "")

        x = 5
        y = 5
        z = 5

        c = Coordinates3D(x, y, z)

        neigh = c.getMooreNeigh(grid)

        expNeigh = [
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

        self.assertEqual(neigh, expNeigh)


if __name__ == '__main__':
    unittest.main()
