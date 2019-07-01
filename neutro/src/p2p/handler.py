from atomic_p2p.utils.communication import Handler as AtomicP2PHandler, Packet


class SyncHandler(AtomicP2PHandler):
    pkt_type = "neutor-sync"

    def __init__(self, peer, callback):
        super(SyncHandler, self).__init__(
            peer=peer, pkt_type=type(self).pkt_type)
        self.callback = callback
    
    
    def on_send_pkt(self, target, msg):
        data = {
            "msg": msg
        }
        return Packet(dst=target, src=self.peer.server_info.host,
                      _hash=self.peer._hash, _type=type(self).pkt_type,
                      _data=data)
    
    def on_recv_pkt(self, src, pkt, conn):
        data = pkt.data
        self.callback(data)
