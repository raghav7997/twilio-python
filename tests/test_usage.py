import unittest

from mock import patch, Mock
from nose.tools import raises

from tests.tools import create_mock_json
from twilio.rest.http import HttpClient
from twilio.rest.resources import Usage
from twilio.rest.resources.usage import UsageTriggers, UsageTrigger


class TestUsage(unittest.TestCase):

    def setUp(self):
        self.client = HttpClient()
        self.base_uri = "https://api.twilio.com/2010-04-01/Accounts/AC123"
        self.account_sid = "AC123"
        self.auth = (self.account_sid, "token")
        self.usage = Usage(self.client, self.base_uri, self.auth)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_daily_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/Daily'.format(self.base_uri)

        self.usage.records.daily.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_monthly_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/Monthly'.format(self.base_uri)

        self.usage.records.monthly.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_yearly_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/Yearly'.format(self.base_uri)

        self.usage.records.yearly.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_today_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/Today'.format(self.base_uri)

        self.usage.records.today.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_yesterday_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/Yesterday'.format(self.base_uri)

        self.usage.records.yesterday.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_last_month_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/LastMonth'.format(self.base_uri)

        self.usage.records.last_month.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_records_this_month_subresource(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        resp.status_code = 200
        request.return_value = resp

        uri = '{}/Usage/Records/ThisMonth'.format(self.base_uri)

        self.usage.records.this_month.list().execute()

        request.assert_called_with('GET', uri, params={},
                                   use_json_extension=True,
                                   auth=self.auth,
                                   client=self.client)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_triggers_update(self, request):
        resp = create_mock_json("tests/resources/usage_triggers_instance.json")
        resp.status_code = 201
        request.return_value = resp

        self.usage.triggers.update(
            "UT123",
            callback_method="GET",
            callback_url="http://",
            friendly_name="new_friendly_name",
        ).execute()

        uri = "{}/Usage/Triggers/{}".format(self.base_uri, "UT123")

        request.assert_called_with("POST", uri, data={
            "FriendlyName": "new_friendly_name",
            "CallbackUrl": "http://",
            "CallbackMethod": "GET"
        }, auth=self.auth, use_json_extension=True, client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_triggers_create(self, request):
        resp = create_mock_json("tests/resources/usage_triggers_instance.json")
        resp.status_code = 201
        request.return_value = resp

        self.usage.triggers.create(
            friendly_name="foo",
            usage_category="sms",
            trigger_by="count",
            recurring="price",
            trigger_value="10.00",
            callback_url="http://www.example.com",
            callback_method="POST"
        ).execute()

        uri = "%s/Usage/Triggers" % self.base_uri
        request.assert_called_with("POST", uri, data={
            "FriendlyName": "foo",
            "UsageCategory": "sms",
            "TriggerBy": "count",
            "Recurring": "price",
            "TriggerValue": "10.00",
            "CallbackUrl": "http://www.example.com",
            "CallbackMethod": "POST"
        }, auth=self.auth, use_json_extension=True, client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_triggers_paging(self, request):
        resp = create_mock_json("tests/resources/usage_triggers_list.json")
        request.return_value = resp

        uri = "%s/Usage/Triggers" % self.base_uri
        self.usage.triggers.list(
            recurring="daily",
            usage_category="sms",
            trigger_by="count"
        ).execute()

        request.assert_called_with("GET", uri, params={
            "Recurring": "daily",
            "UsageCategory": "sms",
            "TriggerBy": "count"
        }, auth=self.auth, use_json_extension=True, client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_records_paging(self, request):
        resp = create_mock_json("tests/resources/usage_records_list.json")
        request.return_value = resp

        uri = "%s/Usage/Records" % self.base_uri
        self.usage.records.list(
            start_date="2012-10-12",
            end_date="2012-10-13",
            category="sms"
        ).execute()

        request.assert_called_with("GET", uri, params={
            "StartDate": "2012-10-12",
            "EndDate": "2012-10-13",
            "Category": "sms"
        }, auth=self.auth, use_json_extension=True, client=self.client)

    @patch("twilio.rest.resources.base.make_twilio_request")
    def test_delete_trigger(self, req):
        resp = Mock()
        resp.content = ""
        resp.status_code = 204
        req.return_value = resp

        triggers = UsageTriggers(self.client, "https://api.twilio.com", self.auth)
        trigger = UsageTrigger(triggers, "UT123")
        trigger.delete().execute()

        uri = "https://api.twilio.com/Usage/Triggers/UT123"
        req.assert_called_with("DELETE", uri,
                               auth=self.auth,
                               use_json_extension=True,
                               client=self.client)

    @raises(AttributeError)
    def test_records_create(self):
        self.usage.records.all.create

    @raises(AttributeError)
    def test_records_delete(self):
        self.usage.records.all.delete

    @raises(AttributeError)
    def test_records_get(self):
        self.usage.records.all.get('abc')
