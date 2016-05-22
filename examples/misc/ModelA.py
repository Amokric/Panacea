from panacea.core.Model import *
from panacea.core.Steppables import *

# Just a general model class used to test xml auto-setup

class EmptyModel(Model):
    def __init__(self, *args):
        super(EmptyModel, self).__init__(*args)

    def setup(self):
        super(EmptyModel, self).setup()

    def teardown(self):
        pass

class IdleHelper(Helper):

    def __init__(self, *args):

        super(IdleHelper,self).__init__(args)
        self.initDummyVar = "lorem"
        self.argOne = self.args[0]
        self.argTwo = self.args[1]

    def stepPrologue(self, model):
        self.dummyVar = "dummy"

    def stepMain(self, model):
        pass

    def stepEpilogue(selfs, model):
        pass

class IdleAgent(Agent):

    def __init__(self, *args):

        if(len(args) == 1):
            args = args[0]

        radius = int(args[0])
        super(IdleAgent, self).__init__(radius)
        self.tag = args[1]

    def stepPrologue(self, model):
        pass

    def stepMain(self, model):
        pass

    def stepEpilogue(selfs, model):
        pass