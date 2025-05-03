from json import loads
from time import gmtime, strftime

import requests
from rest_framework.exceptions import ValidationError

from apps.core.utils import get_absolute_url
from apps.payment.models import Transaction
from apps.payment.providers.ipg.enumerations import GatewayProviderEnum
from apps.payment.providers.ipg.handlers.base import GatewayProviderBase
from apps.payment.providers.ipg.handlers.enumerations import MellatResponseChoice
from apps.payment.providers.ipg.handlers.serializers import MellatVerifySerializer


class Zarrinpal(GatewayProviderBase):
    _terminal_code = None
    _username = None
    _password = None
    _GATEWAY_SLUG = GatewayProviderEnum.ZARRINPAL
    _verification_serializer = MellatVerifySerializer
    _error_messages = dict(MellatResponseChoice.choices)

    def set_default_settings(self):
        for item in ['MERCHANT_CODE']:
            if item not in self.info:
                raise ValidationError()
            setattr(self, f'_{item.lower()}', self.info[item])

    def get_gateway_payment_url(self):
        return f"{self.config.get('START_PAY')}{self.get_reference_number()}"

    def get_pay_data(self):
        return {
            'merchant_id': self._merchant_code,
            'amount': int(self.get_gateway_amount()),
            'description': f"Pay",
            'callback_url': self._get_gateway_callback_url()
        }

    def _pay(self):
        data = self.get_pay_data()
        response = requests.post(
            'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json',
            data=data
        )
        result = response.json()
        try:
            if result['data']['code'] == 100:
                self._set_reference_number(result['data']['authority'])
        except TypeError:
            status_text = self._get_error_messages(result['errors']['code'])
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
        if result == MellatResponseChoice.SUCCESS.value:
            self._set_payment_status(Transaction.StatusChoice.SUCCESS.value)
        elif result in MellatResponseChoice.failure():
            self._set_payment_status(Transaction.StatusChoice.FAILED.value)
        elif (
                result in MellatResponseChoice.canceled()
                or result not in MellatResponseChoice.already_done()
        ):
            self._set_payment_status(Transaction.StatusChoice.CANCELED_BY_USER.value)

    @staticmethod
    def _get_current_time():
        return strftime("%H%M%S")

    @staticmethod
    def _get_current_date():
        return strftime("%Y%m%d", gmtime())

    def _get_sale_reference_id(self):
        extra_information = loads(getattr(self._transaction, 'extra_information', '{}'))
        return extra_information.get('SaleReferenceId', '1')
