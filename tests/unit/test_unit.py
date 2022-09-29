

from chalicelib.core import get_file_url


def test_get_file_url():
    data = {"fileUrl": "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"}
    file_url = get_file_url(data)
    assert file_url == "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"


def test_get_file_url_failed():
    data = {"notFileUrl": "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"}
    file_url = ""
    try:
        file_url = get_file_url(data)
        assert False
    except:
        assert file_url != "https://previews.123rf.com/images/happyroman/happyroman1611/happyroman161100004/67968361-atm-transaction-printed-paper-receipt-bill-vector.jpg"

