from atomic_p2p.peer import Peer as AtomicP2PPeer

from .handler import SyncHandler


class Peer(AtomicP2PPeer):

    def __init__(self, host, name, role, cert, _hash):
        super(Peer, self).__init__(
            host=host, name=name, role=role, cert=cert, _hash=_hash)
    
    def process_sync_data(self, data):
        print("callback {}".format(data))

    def _register_handler(self):
        super(Peer, self)._register_handler()
        installing_handler = [
            SyncHandler(self, self.process_sync_data)
        ]
        for each in installing_handler:
            self.pkt_handlers[each.pkt_type] = each
