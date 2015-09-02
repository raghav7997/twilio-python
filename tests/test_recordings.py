from datetime import date
from mock import patch
from nose.tools import raises, assert_equals, assert_true

from tests.tools import create_mock_json
from twilio.rest.http import HttpClient
from twilio.rest.resources import Recordings, Recording

BASE_URI = "https://api.twilio.com/2010-04-01/Accounts/AC123"
ACCOUNT_SID = "AC123"
AUTH = (ACCOUNT_SID, "token")

RE_SID = "RE19e96a31ed59a5733d2c1c1c69a83a28"

client = HttpClient()
recordings = Recordings(client, BASE_URI, AUTH)


@patch("twilio.rest.resources.base.make_twilio_request")
def test_paging(mock):
    resp = create_mock_json("tests/resources/recordings_list.json")
    mock.return_value = resp

    uri = "%s/Recordings" % (BASE_URI)
    recordings.list(call_sid="CA123", before=date(2010, 12, 5)).execute()
    exp_params = {'CallSid': 'CA123', 'DateCreated<': '2010-12-05'}

    mock.assert_called_with("GET", uri, params=exp_params, auth=AUTH,
                            use_json_extension=True,
                            client=client)


@patch("twilio.rest.resources.base.make_twilio_request")
def test_get(mock):
    resp = create_mock_json("tests/resources/recordings_instance.json")
    mock.return_value = resp

    uri = "%s/Recordings/%s" % (BASE_URI, RE_SID)
    r = recordings.get(RE_SID).execute()

    mock.assert_called_with("GET", uri, auth=AUTH,
                            use_json_extension=True,
                            client=client)

    truri = "%s/Recordings/%s/Transcriptions" % (BASE_URI, RE_SID)
    assert_equals(r.transcriptions.uri, truri)


@patch("twilio.rest.resources.base.make_twilio_request")
def test_delete_list(mock):
    resp = create_mock_json("tests/resources/recordings_instance.json")
    resp.status_code = 204
    mock.return_value = resp

    uri = "%s/Recordings/%s" % (BASE_URI, RE_SID)
    r = recordings.delete(RE_SID).execute()

    mock.assert_called_with("DELETE", uri, auth=AUTH, use_json_extension=True,
                            client=client)
    assert_true(r)


@patch("twilio.rest.resources.base.make_twilio_request")
def test_delete_instance(mock):
    resp = create_mock_json("tests/resources/recordings_instance.json")
    resp.status_code = 204
    mock.return_value = resp

    uri = "%s/Recordings/%s" % (BASE_URI, RE_SID)
    rec = Recording(recordings, RE_SID)
    r = rec.delete().execute()

    mock.assert_called_with("DELETE", uri, auth=AUTH,
                            use_json_extension=True,
                            client=client)
    assert_true(r)


@raises(AttributeError)
def test_create():
    recordings.create


@raises(AttributeError)
def test_update():
    recordings.update
