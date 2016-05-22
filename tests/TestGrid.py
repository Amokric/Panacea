import unittest

import numpy as np
from panacea.core.Grid import *
from panacea.core.Coordinates import *
from panacea.MResModel.TumourAgents import *
from panacea.examples.misc.ModelA import EmptyModel, IdleAgent


class TestGrid(unittest.TestCase):
    def test_numerical_grid_2d_setup(self):
        grid = NumericalGrid2D(5, 7, "")

        size = grid.getSize()

        self.assertEqual(5, size[0])
        self.assertEqual(7, size[1])

    def test_set_get_values_grid_2d(self):
        grid = NumericalGrid2D(5, 5, "")

        coordinates = Coordinates2D(1, 1)

        val = 3

        grid.setGridValue(coordinates, val)
        retrievedValue = grid.getGridValue(coordinates)

        self.assertEquals(val, retrievedValue)

    def test_test_set_all_grid_values_grid_2d(self):
        grid = NumericalGrid2D(5,5,"")

        val = 3

        grid.setAllGridValues(val)

        gridB = numpy.ones((5,5))
        gridB = val*gridB

        self.assertEqual(gridB.all(), grid.grid.all())

    def test_get_moore_neigh_grid_2d(self):
        grid = NumericalGrid2D(5, 5,"")

        c = Coordinates2D(2, 2)

        cA = Coordinates2D(2,3)

        val = 2.

        grid.setGridValue(cA, val)

        neigh = grid.getMooreNeigh(c)

        expNeigh = [
            (Coordinates2D(1, 2), []),
            (Coordinates2D(1, 1), []),
            (Coordinates2D(1, 3), []),
            (Coordinates2D(3, 2), []),
            (Coordinates2D(3, 1), []),
            (Coordinates2D(3, 3), []),
            (Coordinates2D(2, 3), [val]),
            (Coordinates2D(2, 1), [])
        ]

        self.assertEqual(expNeigh, neigh)

        cB = Coordinates2D(1,2)
        cC = Coordinates2D(1,3)

        valB = 4.2
        valC = 0.3

        grid.setGridValue(cB, valB)
        grid.setGridValue(cC, valC)

        neigh = grid.getMooreNeigh(c)

        expNeigh = [
            (Coordinates2D(1, 2), [valB]),
            (Coordinates2D(1, 1), []),
            (Coordinates2D(1, 3), [valC]),
            (Coordinates2D(3, 2), []),
            (Coordinates2D(3, 1), []),
            (Coordinates2D(3, 3), []),
            (Coordinates2D(2, 3), [val]),
            (Coordinates2D(2, 1), [])
        ]

        self.assertEqual(expNeigh, neigh)



    def test_numerical_grid_3d_setup(self):
        grid = NumericalGrid3D(1, 2, 3,"")

        size = grid.getSize()

        self.assertEqual(1, size[0])
        self.assertEqual(2, size[1])
        self.assertEqual(3, size[2])

    def test_set_get_values_grid_3d(self):
        grid = NumericalGrid3D(5, 5, 5,"")

        coordinates = Coordinates3D(1, 2, 3)

        val = 4

        grid.setGridValue(coordinates, val)
        retrievedValue = grid.getGridValue(coordinates)

        self.assertEqual(val, retrievedValue)

    def test_object_grid_2d_setup(self):
        grid = ObjectGrid2D(5, 6,"")

        size = grid.getSize()

        self.assertEqual(5, size[0])
        self.assertEqual(6, size[1])

    def test_set_get_object_grid_2d(self):

        gName = "testGrid"
        grid = ObjectGrid2D(5, 5,gName)

        c = Coordinates2D(4, 4)

        h = HealthyCell()

        grid.moveAgent(c, h)

        self.assertEqual(c, h.gridPositions[gName])

        retrieved = grid.getAtPos(c)

        self.assertEqual([h], retrieved)
        self.assertEqual([(c, h)], grid.gridAgents)

        cB = Coordinates2D(3, 3)

        grid.moveAgent(cB, h)

        retrieved = grid.getAtPos(c)
        retrievedB = grid.getAtPos(cB)

        self.assertEqual([], retrieved)
        self.assertEqual([h], retrievedB)
        self.assertEqual([(cB, h)], grid.gridAgents)

        cC = Coordinates2D(1,3)
        hB = HealthyCell()

        grid.moveAgent(cC, hB)

        retrievedB = grid.getAtPos(cB)
        retrievedC = grid.getAtPos(cC)

        self.assertEqual([h], retrievedB)
        self.assertEqual([hB], retrievedC)
        self.assertEqual([(cB,h),(cC,hB)], grid.gridAgents)

        grid.moveAgent(cC, h)

        retrievedB = grid.getAtPos(cB)
        retrievedC = grid.getAtPos(cC)

        self.assertEqual([], retrievedB)
        self.assertEqual([h, hB], retrievedC)
        self.assertEqual([(cC,h),(cC, hB)], grid.gridAgents)

    def test_get_agent_position_grid_2d(self):
        grid = ObjectGrid2D(5,5,"")

        h = HealthyCell()

        c = Coordinates2D(2,2)

        grid.moveAgent(c,h)

        retrievedLocation = grid.getAgentPosition(h)
        self.assertEqual(c,retrievedLocation)

        cB = Coordinates2D(4,4)
        grid.moveAgent(cB,h)

        retrievedLocation = grid.getAgentPosition(h)
        self.assertEqual(cB,retrievedLocation)

    def test_remove_agent_grid_2d(self):
        grid = ObjectGrid2D(5,5,"")

        h = HealthyCell()

        c = Coordinates2D(2,2)

        grid.moveAgent(c,h)

        retrievedLocation = grid.getAgentPosition(h)
        self.assertEqual(c,retrievedLocation)

        grid.removeAgent(h)


        self.assertEqual([], grid.getAtPos(c))

    def test_get_moore_neigh_grid_2d(self):

        grid = ObjectGrid2D(5, 5,"")

        c = Coordinates2D(2, 2)

        cA = Coordinates2D(2,3)
        h = HealthyCell()

        grid.moveAgent(cA,h)

        neigh = grid.getMooreNeigh(c)

        expNeigh = [
            (Coordinates2D(1, 2), []),
            (Coordinates2D(1, 1), []),
            (Coordinates2D(1, 3), []),
            (Coordinates2D(3, 2), []),
            (Coordinates2D(3, 1), []),
            (Coordinates2D(3, 3), []),
            (Coordinates2D(2, 3), [h]),
            (Coordinates2D(2, 1), [])
        ]

        self.assertEqual(expNeigh, neigh)

        hB = HealthyCell()
        grid.moveAgent(cA,hB)

        neigh = grid.getMooreNeigh(c)

        expNeigh = [
            (Coordinates2D(1, 2), []),
            (Coordinates2D(1, 1), []),
            (Coordinates2D(1, 3), []),
            (Coordinates2D(3, 2), []),
            (Coordinates2D(3, 1), []),
            (Coordinates2D(3, 3), []),
            (Coordinates2D(2, 3), [h, hB]),
            (Coordinates2D(2, 1), [])
        ]

        self.assertEqual(expNeigh, neigh)

        cB = Coordinates2D(1,2)

        hC = HealthyCell()

        grid.moveAgent(cB, hC)

        neigh = grid.getMooreNeigh(c)

        expNeigh = [
            (Coordinates2D(1, 2), [hC]),
            (Coordinates2D(1, 1), []),
            (Coordinates2D(1, 3), []),
            (Coordinates2D(3, 2), []),
            (Coordinates2D(3, 1), []),
            (Coordinates2D(3, 3), []),
            (Coordinates2D(2, 3), [h, hB]),
            (Coordinates2D(2, 1), [])
        ]

        self.assertEqual(expNeigh, neigh)

    def test_get_least_populated_moore_neigh_grid_2d(self):

        grid = ObjectGrid2D(5,5,"")

        c = Coordinates2D(1,1)
        cB = Coordinates2D(1,2)
        cC = Coordinates2D(1,3)
        cD = Coordinates2D(2,1)
        cE = Coordinates2D(2,3)
        cF = Coordinates2D(3,1)
        cG = Coordinates2D(3,3)

        h = HealthyCell()
        hB = HealthyCell()
        hC = HealthyCell()
        hD = HealthyCell()
        hE = HealthyCell()
        hF = HealthyCell()
        hG = HealthyCell()

        grid.moveAgent(c,h)
        grid.moveAgent(cB, hB)
        grid.moveAgent(cC, hC)
        grid.moveAgent(cD, hD)
        grid.moveAgent(cE, hE)
        grid.moveAgent(cF, hF)
        grid.moveAgent(cG, hG)

        cCentral = Coordinates2D(2,2)

        retrievedCoords = grid.getLeastPopulatedMooreNeigh(cCentral)

        self.assertEqual(Coordinates2D(3,2), retrievedCoords)

        hH = HealthyCell()
        grid.moveAgent(c, hH)

        retrievedCoords = grid.getLeastPopulatedMooreNeigh(cCentral)

        self.assertEqual(Coordinates2D(3,2), retrievedCoords)

    def test_get_most_populated_moore_neigh_grid_2d(self):
        grid = ObjectGrid2D(5,5,"")

        h = HealthyCell()

        c = Coordinates2D(1,3)

        grid.moveAgent(c,h)

        cCentral = Coordinates2D(2,2)

        retrievedCoords = grid.getMostPopulatedMooreNeigh(cCentral)

        self.assertEqual(c, retrievedCoords)

        hB = HealthyCell()
        hC = HealthyCell()

        cOther = Coordinates2D(1,2)

        grid.moveAgent(cOther, hB)
        grid.moveAgent(c, hC)

        retrievedCoords = grid.getMostPopulatedMooreNeigh(cCentral)

        self.assertEqual(c, retrievedCoords)

    def test_get_grid_name(self):

        name = "grid one"

        og2d = ObjectGrid2D(5,5, name)
        self.assertEqual(name, og2d.getGridName())

        #og3d = ObjectGrid3D(5,5,5, name)
        #self.assertEqual(name, og3d.getGridName())

        ng2d = NumericalGrid2D(5,5,name)
        self.assertEqual(name, ng2d.getGridName())

        ng3d = NumericalGrid3D(5,5,5,name)
        self.assertEqual(name, ng3d.getGridName())

    def test_grid_larger_radius(self):
        m = EmptyModel("../examples/misc/xmlSetup/setupB.xml", "xml")
        m.setup()

        grid = m.getGridFromName("gridA")
        self.assertEqual(True, isinstance(grid, ObjectGrid2D))
        self.assertEqual((123, 321), grid.getSize())

        agentList = grid.gridAgents
        self.assertEqual(1, len(agentList))

        agent = agentList[0][1]
        self.assertEqual(True, isinstance(agent, IdleAgent))

        self.assertEqual(Coordinates2D(10,10), grid.getAgentPosition(agent))
        self.assertEqual([agent], grid.getAtPos(Coordinates2D(10,10)))

        neigh = Coordinates2D(10,10).getMooreNeigh(grid)

        for n in neigh:
            self.assertEqual([agent], grid.getAtPos(n))

        self.assertEqual([agent], grid.getAtPos(Coordinates2D(8,10)))
        self.assertEqual([], grid.getAtPos(Coordinates2D(7,10)))

        # repeating tests on the second grid
        grid = m.getGridFromName("gridB")

        self.assertEqual(True, isinstance(grid, ObjectGrid2D))
        self.assertEqual((200, 250), grid.getSize())

        agentList = grid.gridAgents
        self.assertEqual(1, len(agentList))

        agent = agentList[0][1]
        self.assertEqual(True, isinstance(agent, IdleAgent))

        self.assertEqual(Coordinates2D(10,10), grid.getAgentPosition(agent))
        self.assertEqual([agent], grid.getAtPos(Coordinates2D(10,10)))

        neigh = Coordinates2D(10,10).getMooreNeigh(grid)

        for n in neigh:
            self.assertEqual([agent], grid.getAtPos(n))

        self.assertEqual([agent], grid.getAtPos(Coordinates2D(8,10)))
        self.assertEqual([], grid.getAtPos(Coordinates2D(7,10)))

    def test_object_grid_3d(self):

        grid = ObjectGrid3D(5,6,7,"test")

        self.assertEqual((5,6,7), grid.getSize())


    def test_object_grid_3d_obj(self):

        grid = ObjectGrid3D(2,2,2,"test")

        self.assertEqual([[[[],[]],[[],[]]],[[[],[]],[[],[]]]], grid.getGrid())

    def test_object_grid_3d_move_agent(self):

        grid = ObjectGrid3D(3,3,3, "test")

        a = IdleAgent(1,"")

        grid.moveAgent(Coordinates3D(2,2,2), a)

        self.assertEqual([a], grid.grid[2][2][2])

    def test_object_grid_3d_get_agent_position(self):

        grid = ObjectGrid3D(3,3,3, "test")

        a = IdleAgent(1,"")

        c = Coordinates3D(2,2,2)

        grid.moveAgent(c, a)

        retrieved = self.assertEqual(c, grid.getAgentPosition(a))

    def test_object_grid_3d_get_agents_at_position(self):

        grid = ObjectGrid3D(5,5,5, "test")

        a = IdleAgent(1,"")

        c = Coordinates3D(2,3,4)

        grid.moveAgent(c,a)

        self.assertEqual([a], grid.getAtPos(c))

        cB = Coordinates3D(3,2,1)

        aB = IdleAgent(1,"")

        grid.moveAgent(cB, a)
        grid.moveAgent(cB, aB)

        self.assertEqual([a, aB], grid.getAtPos(cB))
        self.assertEqual([], grid.getAtPos(c))

    def test_object_grid_3d_remove_agent(self):

        grid = ObjectGrid3D(3,3,3,"")

        a = IdleAgent(1,"")

        c = Coordinates3D(2,2,2)

        grid.moveAgent(c,a)

        self.assertEqual([a], grid.getAtPos(c))

        grid.removeAgent(a)

        self.assertEqual([], grid.getAtPos(c))

    def test_object_grid_3d_most_populated_moore_neigh(self):

        grid = ObjectGrid3D(5,5,5,"")

        a = IdleAgent(1,"")
        aB = IdleAgent(1,"")
        aC = IdleAgent(1,"")

        c = Coordinates3D(2,2,2)
        cB = Coordinates3D(2,2,3)
        cC = Coordinates3D(2,1,2)

        grid.moveAgent(cB,a)

        self.assertEqual(cB, grid.getMostPopulatedMooreNeigh(c))

        grid.moveAgent(cB,aB)
        grid.moveAgent(cC,aC)

        self.assertEqual(cB, grid.getMostPopulatedMooreNeigh(c))

        grid.moveAgent(cC, aB)

        self.assertEqual(cC, grid.getMostPopulatedMooreNeigh(c))

    def test_object_grid_3d_least_populated_moore_neighbourhood(self):

        grid = ObjectGrid3D(5,5,5,"")

        c = Coordinates3D(3,3,3)

        neigh = c.getMooreNeigh(grid)

        for c in neigh:
            a = IdleAgent(1,"")
            grid.moveAgent(c, a)

        cB = Coordinates3D(2,3,3)

        agent = grid.getAtPos(cB)

        grid.removeAgent(agent[0])

        self.assertEqual(cB, grid.getLeastPopulatedMooreNeigh(c))

if __name__ == '__main__':
    unittest.main()
