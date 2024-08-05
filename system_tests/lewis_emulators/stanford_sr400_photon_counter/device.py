from collections import OrderedDict

from lewis.devices import StateMachineDevice

from .states import DefaultState


class SimulatedStanfordSr400PhotonCounter(StateMachineDevice):

    def _initialize_data(self):
        """
        Initialize all of the device's attributes.
        """
        self.count_a = 0
        self.count_b = 0
        self.counting: bool = False
        self.status_byte: int = int("00000010", 2)

    def _get_state_handlers(self):
        return {
            'default': DefaultState(),
        }

    def _get_initial_state(self):
        return 'default'

    def _get_transition_handlers(self):
        return OrderedDict([])

    def get_count_a(self) -> int:
        if self.counting:
            self.count_a = 20
        return self.count_a

    def get_count_b(self) -> int:
        if self.counting:
            self.count_b = 15
        return self.count_b
    
    def get_status(self) -> int:
        return self.status_byte
    
    def start_counting(self) -> None:
        self.counting = True

    def stop_counting(self) -> None:
        # if this is called twice consequitively reset
        if self.counting:
            self.counting = False
        else:
            self.reset_counter()

    def reset_counter(self):
        self.count_a = 0
        self.count_b = 0
        self.counting = False
        self.status_byte = int("00000010", 2)
