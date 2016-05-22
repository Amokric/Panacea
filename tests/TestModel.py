import unittest

from panacea.MResModel.TumourModel import TumourModel


class TestModel(unittest.TestCase):

    def test_model_setup(self):
        ep = 12
        m = TumourModel()
        m.setEpochs(ep)
        self.assertEqual(ep, m.getEpochs())

if __name__ == '__main__':
    unittest.main()