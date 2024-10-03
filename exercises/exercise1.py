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
            destination = (self.index()+1) % (self.number_of_devices())
            
            if self.index() == 0:
                message = GossipMessage(self.index(), destination, self._secrets)
                self.medium().send(message)

            ingoing = self.medium().receive()
            while ingoing is None:
                ingoing = self.medium().receive()
            self._secrets = self._secrets.union(ingoing.secrets)
            message = GossipMessage(self.index(), destination, self._secrets.union(ingoing.secrets))
            self.medium().send(message)

            if len(self._secrets) == self.number_of_devices():
                print(f"Device {self.index()} got all secrets")
                break

            

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')
