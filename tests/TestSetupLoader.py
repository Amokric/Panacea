import unittest

from panacea.core.Coordinates import Coordinates2D
from panacea.core.Grid import ObjectGrid2D, NumericalGrid2D
from panacea.examples.gameOfLife.GameOfLife import GOLModelAutoSetup
from panacea.examples.misc.ModelA import *
from panacea.examples.particleSwarmOptimization.ParticleSwarmOptimization import PSOModelAutoSetup, PSOAgent, \
    ParticleSwarmOptimizationRenderer


class TestSetuploader(unittest.TestCase):

    def test_model_setup(self):
        golModel = GOLModelAutoSetup("../examples/gameOfLife/xmlSetup/golSetupSimpleTest.xml", "xml")
        golModel.setup()

        g = golModel.getGridFromName("golgrid")
        gSize = g.getSize()
        self.assertEqual((100,100), gSize)

        agents = g.getAtPos(Coordinates2D(5,7))

        self.assertEqual(1, len(agents))

        agent = agents[0]

        self.assertEqual(1, agent.getRadius())
        self.assertEqual(0, agent.state)

    def test_model_setup_ext(self):
        golModel = GOLModelAutoSetup("../examples/gameOfLife/xmlSetup/setupSmallModel.xml", "xml")
        golModel.setup()

        g = golModel.getGridFromName("golgrid")
        gSize = g.getSize()
        self.assertEqual((3,3), gSize)

        center = Coordinates2D(1,1)
        centerNeigh = g.getMooreNeigh(center)

        for n in centerNeigh:
            tempAgentList = n[1]
            self.assertEqual(1, len(tempAgentList))

            tempAgent = tempAgentList[0]
            self.assertEqual(1, tempAgent.getRadius())


    def test_model_setup_A(self):

        m = EmptyModel("../examples/misc/xmlSetup/setupA.xml", "xml")
        m.setup()

        grids = m.grids

        self.assertEqual(2, len(grids))

        gA = m.getGridFromName("gridA")
        self.assertEqual((123,321),gA.getSize())

        gB = m.getGridFromName("gridB")
        self.assertEqual((200,250), gB.getSize())

        agentListA = gA.getAtPos(Coordinates2D(0,0))
        agentListB = gA.getAtPos(Coordinates2D(1,1))

        self.assertEqual(1, len(agentListA))
        self.assertEqual(0, len(agentListB))

        agentListC = gB.getAtPos(Coordinates2D(2,3))
        self.assertEqual(1, len(agentListC))

        idleAgentA = agentListC[0]

        self.assertEqual(1, idleAgentA.radius)
        self.assertEqual("tagA", idleAgentA.tag)

        agentListD = gA.getAtPos(Coordinates2D(1,5))
        self.assertEqual(2, len(agentListD))

        idleAgentB = agentListD[0]

        retrievedPosB = gB.getAtPos(Coordinates2D(7,8))
        self.assertEqual(idleAgentB, retrievedPosB[0])

        self.assertEqual(idleAgentB.tag, "tagB")

        idleAgentC = agentListD[1]

        retrievedPosC = gB.getAtPos(Coordinates2D(9,10))

        self.assertEqual(idleAgentC, retrievedPosC[0])

        self.assertEqual(idleAgentC.tag, "tagC")

        # checking that the helper has actually been added
        helpers = m.schedule.helpers

        self.assertEqual(1, len(helpers))

        helper = helpers[0]

        self.assertEqual("IdleHelper", helper.__class__.__name__)
        self.assertEqual("lorem", helper.initDummyVar)
        helper.stepPrologue(m)
        self.assertEqual("dummy", helper.dummyVar)

        self.assertEqual("dummy", helper.argOne)
        self.assertEqual("anotherDummy", helper.argTwo)

    def test_pso_model(self):
        m = PSOModelAutoSetup("../examples/particleSwarmOptimization/xmlSetup/setup.xml", "xml")
        m.setup()

        optionalParams = m.optionalParameters

        self.assertEqual(50, optionalParams["food location x"])
        self.assertEqual(60, optionalParams["food location y"])

        self.assertEqual(m.foodLocation, Coordinates2D(50,60))

        grid = m.getGridFromName("psogrid")

        self.assertEqual(True, isinstance(grid, ObjectGrid2D))

        self.assertEqual((100,100), grid.getSize())

        agentListA = grid.getAtPos(Coordinates2D(10,10))
        self.assertEqual(1, len(agentListA))

        agent = agentListA[0]
        self.assertEqual(True, isinstance(agent, PSOAgent))

        helper = m.schedule.helpers[0]

        self.assertEqual(True, isinstance(helper, ParticleSwarmOptimizationRenderer))
        self.assertEqual("psogrid", grid.gridName)

    def test_load_numerical_grid(self):
        m = EmptyModel("../examples/misc/xmlSetup/setupB.xml", "xml")
        m.setup()

        grid = m.getGridFromName("gridC")

        self.assertEqual(True, isinstance(grid, NumericalGrid2D))

        self.assertEqual((123,456), grid.getSize())
        self.assertEqual(12, grid.getGridValue(Coordinates2D(1,1)))
        self.assertEqual(15, grid.getGridValue(Coordinates2D(9,10)))
        self.assertEqual(12, grid.getGridValue(Coordinates2D(1,1)))

if __name__ == '__main__':
    unittest.main()