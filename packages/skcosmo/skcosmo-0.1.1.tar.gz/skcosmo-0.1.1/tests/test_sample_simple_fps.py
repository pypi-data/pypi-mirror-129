import unittest

from sklearn.datasets import load_boston
from sklearn.utils.validation import NotFittedError

from skcosmo.sample_selection import FPS


class TestFPS(unittest.TestCase):
    def setUp(self):
        self.X, _ = load_boston(return_X_y=True)
        self.idx = [0, 410, 492, 102, 134, 413, 54, 32, 353, 126]

    def test_restart(self):
        """
        This test checks that the model can be restarted with a new number of
        samples and `warm_start`
        """

        selector = FPS(n_to_select=1, initialize=self.idx[0])
        selector.fit(self.X)

        for i in range(2, len(self.idx)):
            selector.n_to_select = i
            selector.fit(self.X, warm_start=True)
            self.assertEqual(selector.selected_idx_[i - 1], self.idx[i - 1])

    def test_initialize(self):
        """
        This test checks that the model can be initialized in all applicable manners
        and throws an error otherwise
        """

        for initialize in [self.idx[0], "random"]:
            with self.subTest(initialize=initialize):
                selector = FPS(n_to_select=1, initialize=initialize)
                selector.fit(self.X)

        initialize = self.idx[:4]
        with self.subTest(initialize=initialize):
            selector = FPS(n_to_select=len(self.idx) - 1, initialize=initialize)
            selector.fit(self.X)
            for i in range(4):
                self.assertEqual(selector.selected_idx_[i], self.idx[i])

        with self.assertRaises(ValueError) as cm:
            selector = FPS(n_to_select=1, initialize="bad")
            selector.fit(self.X)
            self.assertEquals(
                str(cm.message), "Invalid value of the initialize parameter"
            )

    def test_get_distances(self):
        """
        This test checks that the haussdorf distances are returnable after fitting
        """
        selector = FPS(n_to_select=1)
        selector.fit(self.X)
        _ = selector.get_select_distance()

        with self.assertRaises(NotFittedError):
            selector = FPS(n_to_select=1)
            _ = selector.get_select_distance()


if __name__ == "__main__":
    unittest.main(verbosity=2)
