from json import dumps, loads
from time import gmtime, strftime

from django.conf import settings
from rest_framework.exceptions import ValidationError
from zeep import Client, Transport

from apps.payment.providers.ipg.handlers.base import GatewayProviderBase
from apps.payment.providers.ipg.handlers.enumerations import MellatResponseChoice
from apps.payment.providers.ipg.handlers.serializers import MellatVerifySerializer
from apps.payment.models import Transaction


class Mellat(GatewayProviderBase):
    _terminal_code = None
    _username = None
    _password = None
    _verification_serializer = MellatVerifySerializer
    _error_messages = dict(MellatResponseChoice.choices)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._payment_url = settings.MELLAT_PAYMENT_URL

    def set_default_settings(self):
        for item in ['TERMINAL_CODE', 'USERNAME', 'PASSWORD']:
            if item not in self.info:
                raise ValidationError()
            setattr(self, f'_{item.lower()}', self.default_setting_kwargs[item])

    def _get_gateway_payment_parameter(self):
        return {
            'RefId': self.get_reference_number(),
            'MobileNo': self.get_mobile_number()
        }

    def get_pay_data(self):
        return {
            'terminalId': int(self._terminal_code),
            'userName': self._username,
            'userPassword': self._password,
            'orderId': int(self.get_tracking_code()),
            'amount': int(self.get_gateway_amount()),
            'localDate': self._get_current_date(),
            'localTime': self._get_current_time(),
            'additionalData': 'خرید با شماره پیگیری - {}'.format(self.get_tracking_code()),
            'callBackUrl': self._get_gateway_callback_url(),
            'payerId': 0
        }

    def _pay(self):
        data = self.get_pay_data()
        client = self._get_client()
        response = client.service.bpPayRequest(**data)
        try:
            status, reference_number = response.split(',')
            if status == MellatResponseEnum.SUCCESS:
                self._set_reference_number(reference_number)
        except ValueError:
            status_text = self._get_error_messages(response)
            self._set_transaction_status_text(status_text)
            raise ValidationError(self.get_transaction_status_text())

    def prepare_verify_from_gateway(self, **validated_data):
        reference_number = validated_data.get('RefId')
        tracking_code = validated_data.get('SaleOrderId')

        self._set_reference_number(reference_number)
        self._set_tracking_code(tracking_code)

    def get_verify_data(self):
        return {
            'terminalId': self._terminal_code,
            'userName': self._username,
            'userPassword': self._password,
            'orderId': self.get_tracking_code(),
            'saleOrderId': self.get_tracking_code(),
            'saleReferenceId': self._get_sale_reference_id()
        }

    def _verify(self, transaction_code):
        data = self.get_verify_data()
        client = self._get_client()
        result = client.service.bpVerifyRequest(**data)
        if result == MellatResponseEnum.SUCCESS:
            self._set_payment_status(Transaction.StatusChoice.SUCCESS.value)
        elif result in MellatResponseEnum.failure():
            self._set_payment_status(Transaction.StatusChoice.FAILED.value)
        elif (
                result in MellatResponseEnum.canceled()
                or result not in MellatResponseEnum.already_done()
        ):
            self._set_payment_status(Transaction.StatusChoice.CANCELED_BY_USER.value)

    def _get_client(self):
        transport = Transport(timeout=5, operation_timeout=5)
        return Client(self.config.get('GATEWAY_CLIENT'), transport=transport)

    @staticmethod
    def _get_current_time():
        return strftime("%H%M%S")

    @staticmethod
    def _get_current_date():
        return strftime("%Y%m%d", gmtime())

    def _get_sale_reference_id(self):
        extra_information = loads(getattr(self._transaction, 'extra_information', '{}'))
        return extra_information.get('SaleReferenceId', '1')
