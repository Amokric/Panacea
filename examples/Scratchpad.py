
from panacea.examples.gameOfLife.GameOfLife import GOLCell, GOLModel, GOLModelAutoSetup
from panacea.core.utils.SetupLoader import *


#xmlLoader = XMLLoader("../examples/gameOfLife/golSetupSimpleTest.xml", GOLModel())

model = GOLModelAutoSetup("../examples/gameOfLife/xmlSetup/setupSmallModel.xml", "xml")
model = GOLModel()

model.simulateModel()
from panacea.examples.particleSwarmOptimization.ParticleSwarmOptimization import PSOModelAutoSetup

#m = PSOModelAutoSetup("../examples/particleSwarmOptimization/xmlSetup/setup.xml", "xml")
#m.simulateModel()


