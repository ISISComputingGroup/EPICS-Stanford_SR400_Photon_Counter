from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply

from ..device import SimulatedStanfordSr400PhotonCounter

@has_log
class StanfordSr400PhotonCounterStreamInterface(StreamInterface):
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(StanfordSr400PhotonCounterStreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.get_status).escape("SS").eos().build(),
            CmdBuilder(self.start_counting).escape("CS").eos().build(),
            CmdBuilder(self.stop_counting).escape("CH").eos().build(),
            CmdBuilder(self.reset_counter).escape("CR").eos().build(),
            CmdBuilder(self.get_counter_a).escape("QA").eos().build(),
            CmdBuilder(self.get_counter_b).escape("QB").eos().build(),
        }

        self.device: SimulatedStanfordSr400PhotonCounter = self.device

    def get_counter_a(self) -> int:
        return self.device.get_count_a()
    
    def get_counter_b(self) -> int:
        return self.device.get_count_b()
    
    def get_status(self):
        return self.device.get_status()
    
    def start_counting(self):
        self.device.start_counting()
    
    def stop_counting(self):
        self.device.stop_counting()

    def reset_counter(self):
        self.device.reset_counter()
    
    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))
