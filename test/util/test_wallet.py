import pytest

from src.util.wallet import Wallet
from src.util import wallet
from src.database import wallet_database
from src.chain.transaction import Transaction


def test_generate_wallet():
    # test generating new wallet
    try:
        w1 = Wallet()
        # test loading wallet
        w2 = Wallet(w1.get_address())
        # make sure these are the same
        assert w1.get_address() == w2.get_address()
        assert w1.get_public_key().to_pem() == w2.get_public_key().to_pem()
        assert w1.get_private_key().to_pem() == w2.get_private_key().to_pem()
    finally:
        # remove the wallet
        wallet_database.remove_wallet(w1.get_address())


def test_load_non_existent_wallet():
    # test that only existent wallets can be loaded
    with pytest.raises(ValueError):
        w3 = Wallet("non_valid_address")


def test_generate_wallet_wrong_argument():
    # test that wallets can only be created with strings
    with pytest.raises(ValueError):
        w = Wallet(1)


def test_sign_transaction():
    # test if transactions can be signed
    try:
        w = Wallet()
        t = Transaction(sender=w.get_address(), receivers=[
            "01"], amounts=[1], nonce=1, fee=100)

        public_key = w.get_public_key()
        signature = w.sign_transaction(t)

        assert t.verify()
    finally:
        wallet_database.remove_wallet(w.get_address())


def test_sign_unvalid_tx():
    # test if signing unvalid transaction is rejected
    try:
        w = Wallet()
        t = Transaction(sender="different sender than wallet", receivers=[
            "01"], amounts=[1], nonce=1, fee=100)

        with pytest.raises(ValueError):
            w.sign_transaction(t)
    finally:
        wallet_database.remove_wallet(w.get_address())


def test_nonce_correctly():
    # test if the nonce increases when signing a tx
    # test if loaded wallet (w_copy) has correct nonce
    try:
        w = Wallet()
        t = Transaction(sender=w.get_address(), receivers=[
            "01"], amounts=[1], nonce=1, fee=100)
        assert w.get_nonce() == 0
        w.sign_transaction(t)
        assert w.get_nonce() == 1
        w_copy = Wallet(w.get_address())
        assert w_copy.get_nonce() == 1
    finally:
        wallet_database.remove_wallet(w.get_address())


def test_nonce_in_tx_correct():
    # test if the nonce is correct in the tx
    try:
        w = Wallet()
        t = Transaction(sender=w.get_address(), receivers=[
            "01"], amounts=[1], nonce=w.get_nonce(), fee=100)
        assert t.nonce == w.get_nonce()

        tx_hash_old = ""
        tx_sig_old = ""
        for i in range(10):
            # sign tx
            w.sign_transaction(t)
            # get sig
            signature = t.get_signature()
            # nonce gets bigger every signed tx
            assert t.nonce == w.get_nonce() - 1
            assert t.nonce == i
            # make sure tx_signature changes
            assert signature != tx_sig_old
            # make sure tx_hash changes
            assert t.hash() != tx_hash_old
            # finally test if verify works
            assert t.verify()
            # save values for next iteration
            tx_hash_old = t.hash()
            tx_sig_old = signature
        # assert that we counted correctly
        assert w.get_nonce() == 10
    finally:
        wallet_database.remove_wallet(w.get_address())
