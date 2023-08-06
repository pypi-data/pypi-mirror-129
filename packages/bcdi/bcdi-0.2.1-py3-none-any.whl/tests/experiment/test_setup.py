# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-05/2021 : DESY PHOTON SCIENCE
#   (c) 06/2021-present : DESY CFEL
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

import numpy as np
import unittest
from bcdi.experiment.setup import Setup


def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


class Test(unittest.TestCase):
    """Tests related to setup instantiation."""

    def test_instantiation_missing_parameter(self):
        with self.assertRaises(TypeError):
            Setup()


class TestCheckSetup(unittest.TestCase):
    """
    Tests related to check_setup.

        def check_setup(
        self,
        grazing_angle: Optional[Tuple[Real, ...]],
        inplane_angle: Union[Real, np.ndarray],
        outofplane_angle: Union[Real, np.ndarray],
        tilt_angle: np.ndarray,
        detector_distance: Real,
        energy: Union[Real, np.ndarray],
    ) -> None:
    """

    def setUp(self) -> None:
        self.setup = Setup(beamline="ID01")
        self.params = {
            "grazing_angle": (1, 2),
            "inplane_angle": 1.23,
            "outofplane_angle": 49.2,
            "tilt_angle": np.array([1, 1.005, 1.01, 1.015]),
            "detector_distance": 0.5,
            "energy": 9000,
        }

    def test_check_setup_distance_predefined(self):
        self.setup.distance = 1.5
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.distance, 1.5)

    def test_check_setup_distance_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.distance, self.params["detector_distance"])

    def test_check_setup_distance_undefined(self):
        self.params["detector_distance"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_distance_ndarray(self):
        self.params["distance"] = np.array([1, 1.2, 1.4])
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_energy_predefined(self):
        self.setup.energy = 12000
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.energy, 12000)

    def test_check_setup_energy_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.energy, self.params["energy"])

    def test_check_setup_energy_undefined(self):
        self.params["energy"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_energy_ndarray(self):
        self.params["energy"] = np.array([10.005, 10.010, 10.015])
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_tilt_angle_predefined(self):
        self.setup.tilt_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.tilt_angle, 2)

    def test_check_setup_tilt_angle_none(self):
        self.setup.check_setup(**self.params)
        correct = np.mean(
            self.params["tilt_angle"][1:] - self.params["tilt_angle"][:-1]
        )
        self.assertEqual(self.setup.tilt_angle, correct)

    def test_check_setup_tilt_angle_undefined(self):
        self.params["tilt_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_outofplane_angle_predefined(self):
        self.setup.outofplane_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.outofplane_angle, 2)

    def test_check_setup_outofplane_angle_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.outofplane_angle, self.params["outofplane_angle"])

    def test_check_setup_outofplane_angle_ndarray(self):
        self.params["outofplane_angle"] = np.arange(10)
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_outofplane_angle_undefined(self):
        self.params["outofplane_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_inplane_angle_predefined(self):
        self.setup.inplane_angle = 2
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.inplane_angle, 2)

    def test_check_setup_inplane_angle_none(self):
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.inplane_angle, self.params["inplane_angle"])

    def test_check_setup_inplane_angle_ndarray(self):
        self.params["inplane_angle"] = np.arange(10)
        with self.assertRaises(TypeError):
            self.setup.check_setup(**self.params)

    def test_check_setup_inplane_angle_undefined(self):
        self.params["inplane_angle"] = None
        with self.assertRaises(ValueError):
            self.setup.check_setup(**self.params)

    def test_check_setup_grazing_angle_predefined(self):
        self.setup.grazing_angle = (0.1,)
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.grazing_angle, self.params["grazing_angle"])

    def test_check_setup_grazing_angle_None(self):
        self.setup.grazing_angle = (0.1,)
        self.params["grazing_angle"] = None
        self.setup.check_setup(**self.params)
        self.assertEqual(self.setup.grazing_angle, None)


if __name__ == "__main__":
    run_tests(Test)
    run_tests(TestCheckSetup)
