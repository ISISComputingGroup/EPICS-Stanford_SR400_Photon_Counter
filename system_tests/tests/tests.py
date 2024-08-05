import unittest

from utils.channel_access import ChannelAccess
from utils.ioc_launcher import get_default_ioc_dir
from utils.test_modes import TestModes
from utils.testing import get_running_lewis_and_ioc

DEVICE_PREFIX = "SR400_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("SR400"),
        "macros": {},
        "emulator": "stanford_sr400_photon_counter",
    },
]


TEST_MODES = [ TestModes.DEVSIM]


class StanfordSr400PhotonCounterTests(unittest.TestCase):
    """
    Tests for the _Device_ IOC.
    """
    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("stanford_sr400_photon_counter", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX)

        self._simulate_restart_button_press()

    def _simulate_start_button_press(self):
        self.ca.set_pv_value("START_COUNTING", 1)

    def _simulate_stop_button_press(self):
        self.ca.set_pv_value("STOP_COUNTING", 1)

    def _simulate_restart_button_press(self):
        self.ca.set_pv_value("RESET_COUNTERS", 1)
    
    def test_counters_start(self):
        self.ca.assert_that_pv_is("COUNTER:A:RBV", 0, timeout=2)
        self.ca.assert_that_pv_is("COUNTER:B:RBV", 0, timeout=2)

        self._simulate_start_button_press()

        self.ca.assert_that_pv_is_not("COUNTER:A:RBV", 0, timeout=2)
        self.ca.assert_that_pv_is_not("COUNTER:B:RBV", 0, timeout=2)
    
    def test_counters_stop(self):
        self._simulate_start_button_press()  # The fact that this works has been tested above

        self._simulate_stop_button_press()

        a_val = self.ca.get_pv_value("COUNTER:A:RBV")
        b_val = self.ca.get_pv_value("COUNTER:B:RBV")

        self.ca.assert_that_pv_is("COUNTER:A:RBV", a_val)
        self.ca.assert_that_pv_is("COUNTER:B:RBV", b_val)

    def test_counters_restart(self):
        self._simulate_start_button_press()  # The fact that this works has been tested above

        self._simulate_restart_button_press()  # The fact that this works has been tested above

        self.ca.assert_that_pv_is("COUNTER:A:RBV", 0)
        self.ca.assert_that_pv_is("COUNTER:B:RBV", 0)

    def test_status_changes(self):
        self._simulate_start_button_press()  # The fact that this works has been tested above
        self._lewis.backdoor_set_on_device("status_byte", int("00000100", 2))
        status = self.ca.get_pv_value("STATUS")
        self.ca.assert_that_pv_is("STATUS", int("00000100", 2))

        self._lewis.backdoor_set_on_device("status_byte", int("00000010", 2))
        status = self.ca.get_pv_value("STATUS")

        self.ca.assert_that_pv_is("STATUS", int("00000010", 2))

