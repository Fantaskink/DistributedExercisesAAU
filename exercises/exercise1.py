from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])


    def run(self):
        while True:
            for i in range(0, self.number_of_devices()):
                if i == self.index():
                    continue
                message = GossipMessage(self.index(), i, self._secrets)
                self.medium().send(message)

            ingoing = self.medium().receive()
            if ingoing is None:
                continue
            self._secrets.update(ingoing.secrets)

            print(f"secrets: {self._secrets} num devices: {self.number_of_devices()}")
            if len(self._secrets) == self.number_of_devices():
                print(f"Device {self.index()} got all secrets")
                break

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
