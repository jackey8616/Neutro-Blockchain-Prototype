import socket
socket.SO_REUSEPORT = 15


from atomic_p2p.peer.communication import MessageHandler
from neutro.src.p2p.p2p_api import *
from neutro.src.chain.transaction import Transaction


def test_creating_peer():
    peer = create_a_peer(role='role', name='name', host=('0.0.0.0', 8000))
    assert peer.stopped.is_set() is False
    stop_peer_thread(peer)


def test_join_peers():
    peer_1 = create_a_peer(role='role', name='peer1', host=('0.0.0.0', 8000))
    peer_2 = create_a_peer(role='role', name='peer2', host=('0.0.0.0', 8001))
    join_peers(peer_1, peer_2)
    time.sleep(4)
    assert peer_2.server_info in peer_1.connectlist

    time.sleep(4)
    stop_peer_thread(peer_1)
    stop_peer_thread(peer_2)


def test_stopping_peer():
    peer = create_a_peer(role='role', name='name', host=('0.0.0.0', 8000))
    assert peer.stopped.is_set() is False
    stop_peer_thread(peer)
    assert peer.stopped.is_set() is True


def test_list_peers_in_net():
    peer_1 = create_a_peer(role='role', name='peer1', host=('0.0.0.0', 8000))
    peer_2 = create_a_peer(role='role', name='peer2', host=('0.0.0.0', 8001))
    join_peers(peer_1, peer_2)
    time.sleep(4)
    list_of_peers = len(list_peers_in_net(peer_1))
    assert list_of_peers == 1

    time.sleep(4)
    stop_peer_thread(peer_1)
    stop_peer_thread(peer_2)


def test_send_broadcast():
    # creates a dictionary for nodes
    node = dict()
    # creates a core peer
    node['core_1'] = create_a_peer(role='core', name='core_1', host=('127.0.0.1', 8000))
    # create switch peers
    node['switch_1'] = create_a_peer(role='sw', name='switch_1', host=('127.0.0.1', 8011))
    node['switch_2'] = create_a_peer(role='sw', name='switch_2', host=('127.0.0.1', 8012))
    node['switch_3'] = create_a_peer(role='sw', name='switch_3', host=('127.0.0.1', 8013))
    node['switch_4'] = create_a_peer(role='sw', name='switch_4', host=('127.0.0.1', 8014))
    node['switch_5'] = create_a_peer(role='sw', name='switch_5', host=('127.0.0.1', 8015))
    node['switch_6'] = create_a_peer(role='sw', name='switch_6', host=('127.0.0.1', 8016))

    join_peers(node['switch_1'], node['core_1'])
    join_peers(node['switch_2'], node['core_1'])
    join_peers(node['switch_3'], node['core_1'])
    join_peers(node['switch_4'], node['core_1'])
    join_peers(node['switch_5'], node['switch_4'])
    join_peers(node['switch_6'], node['switch_4'])

    # wait for all threads to complete the join process
    time.sleep(5)

    def json_string_transaction():
        """base test for transaction"""
        sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
        receivers = ["01", "02", "0a"]
        amounts = [1, 2, 3]
        nonce = 1
        fee = 100
        tx = Transaction(sender, receivers, amounts, nonce, fee)

        tx_string = tx.string()
        return tx_string

    json_string_transaction_message = json_string_transaction()

    send_broadcast(node, node['core_1'], json_string_transaction_message)

    time.sleep(5)
    for (key, val) in node.items():
        stop_peer_thread(val)
        time.sleep(2)


def test_send_transaction_direct():
    peer_1 = create_a_peer(role='role', name='peer1', host=('0.0.0.0', 8000))
    peer_2 = create_a_peer(role='role', name='peer2', host=('0.0.0.0', 8001))
    join_peers(peer_1, peer_2)

    time.sleep(4)
    def json_string_transaction():
        """base test for transaction"""
        sender = "iWVjc8hWuRuePAv1X8nDZdcjKcqivDUH62YKhBXBHqp2yGfgeXyHJDj5XwCHwjWB6GevCjMYT59XSBiQvMYHQ4P"
        receivers = ["01", "02", "0a"]
        amounts = [1, 2, 3]
        nonce = 1
        fee = 100
        tx = Transaction(sender, receivers, amounts, nonce, fee)

        tx_string = tx.string()
        return tx_string

    json_string_transaction_message = json_string_transaction()
    send_transaction_direct(json_string_transaction_message, peer_1, peer_2)

    time.sleep(5)
    stop_peer_thread(peer_1)
    stop_peer_thread(peer_2)
