from abc import abstractmethod
from urllib import parse

from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.core.utils import get_absolute_url, gettext_lazy as _
from apps.payment.enumerations import CurrencyChoice
from apps.payment.enumerations import MIN_PAYMENT_AMOUNT
from apps.payment.models import Payment, Transaction, Gateway
from apps.payment.providers.ipg import default_settings as settings
from apps.payment.providers.utils import append_querystring, generate_tracking_code, base64_encode
from apps.service_manager.hooks import use

transaction_services = use('apps.payment.services', 'transaction')
payment_services = use('apps.payment.services', 'payment')
gateway_services = use('apps.payment.services', 'gateway')
wallet_services = use('apps.wallet.services')


class GatewayProviderBase:
    _gateway_currency = CurrencyChoice.IRR.value
    _currency = CurrencyChoice.IRT.value
    _amount = 0
    _platform = 0
    _gateway_amount = 0
    _mobile_number = None
    _tracking_code = None
    _reference_number = ''
    _transaction_status_text = ''
    _client_callback_url = ''
    _transaction = None
    _paying_user = None
    _MIN_AMOUNT = MIN_PAYMENT_AMOUNT
    _GATEWAY_SLUG = None
    _verification_serializer = None
    _error_messages = dict()

    def __init__(self, **kwargs):
        self.info = kwargs.get('info')
        self.config = kwargs.get('config')
        self.default_setting_kwargs = kwargs
        self.set_default_settings()

    @abstractmethod
    def _pay(self):
        raise NotImplementedError()

    @abstractmethod
    def set_default_settings(self):
        raise NotImplementedError()

    @abstractmethod
    def get_pay_data(self):
        raise NotImplementedError()

    @abstractmethod
    def get_verify_data(self):
        raise NotImplementedError()

    @abstractmethod
    def _verify(self, tracking_code):
        raise NotImplementedError()

    @abstractmethod
    def prepare_verify_from_gateway(self, **validated_data):
        raise NotImplementedError()

    @abstractmethod
    def get_gateway_payment_url(self):
        raise NotImplementedError

    def prepare_amount(self):
        if self._currency == self._gateway_currency:
            self._gateway_amount = self._amount
        elif (
                self._currency == CurrencyChoice.IRR.value
                and self._gateway_currency == CurrencyChoice.IRT.value
        ):
            self._gateway_amount = payment_services.get_tomans(self._amount)
        elif (
                self._currency == CurrencyChoice.IRT.value
                and self._gateway_currency == CurrencyChoice.IRR.value
        ):
            self._gateway_amount = payment_services.get_rials(self._amount)
        else:
            self._gateway_amount = self._amount

        if not self.check_amount():
            raise ValidationError('Provided amount is invalid.')

    def check_amount(self):
        return self.get_gateway_amount() >= self.get_minimum_amount()

    def get_paying_amount(self):
        return self._amount

    def set_paying_amount(self, amount):
        if isinstance(amount, str) and not amount.isdigit():
            raise ValidationError(_('Amount must be an integer.'))

        amount = int(amount)
        if amount <= 0:
            raise ValidationError(_('Amount must be a positive integer.'))

        self._amount = amount

    def get_platform(self):
        return self._platform

    def set_platform(self, platform):
        self._platform = platform

    def pay(self, payment):
        self.ready(payment)
        self._pay()
        return self.redirect_gateway()

    def verify(self, tracking_code):
        self._set_tracking_code(tracking_code)
        try:
            self._transaction = transaction_services.get_transaction(
                reference_number=self.get_reference_number(),
                tracking_code=self.get_tracking_code(),
            )

        except Transaction.DoesNotExist:
            raise ValidationError(
                _(
                    'Transaction with reference number [{reference}] and tracking code [{tracking}]'
                    ' does not exist for bank type [{bank}].'
                ).format(
                    reference=self.get_reference_number(), tracking=self.get_tracking_code(),
                    bank=self._GATEWAY_SLUG
                )
            )

        self.get_paying_amount()
        self.prepare_amount()
        self._verify(tracking_code)

    def ready(self, payment):
        self._set_tracking_code(generate_tracking_code())
        self.prepare_amount()
        self._transaction = transaction_services.create_transaction(
            payment=payment,
            source_account=gateway_services.get_gateway(
                mode=Gateway.ModeChoice.ONLINE.value, type=Gateway.TypeChoice.IPG.value,
                is_active=True, slug=self._GATEWAY_SLUG
            ),
            destination_account=wallet_services.get_wallet(
                user=self.get_paying_user(), raise_exception=True
            ),
            amount=self.get_paying_amount(),
            through=Transaction.ThroughChoice.GATEWAY.value,
            tracking_code=self.get_tracking_code(),
            reference_number=self.get_reference_number(),
            response_result=self.get_transaction_status_text(),
            callback_url=self._client_callback_url,
            # modifier_user=self.get_paying_user()
        )

    def verify_from_gateway(self, paying_user, data):
        validated_data = self._get_verification_inputs(data)
        self.set_paying_user(paying_user)
        self.prepare_verify_from_gateway(**validated_data)
        if (
                self.transaction is not None
                and self.transaction.status == Transaction.StatusChoice.REDIRECT_TO_BANK.value
        ):
            if (
                    self.transaction.payment.status != Payment.StatusChoice.PENDING.value
                    or self.transaction.payment.remaining_of_payment == 0
            ):
                self._set_payment_status(Transaction.StatusChoice.FAILED.value)
                return False
            else:
                self._set_payment_status(Transaction.StatusChoice.RETURN_FROM_BANK.value)
                self.verify(self.get_tracking_code())
                return True

        return False

    def get_client_callback_url(self):
        return append_querystring(
            self._transaction.callback_url,
            {
                settings.TRACKING_CODE_QUERY_PARAM: self.get_tracking_code()
            }
        )

    def redirect_client_callback(self):
        return redirect(self.get_client_callback_url())

    def set_mobile_number(self, mobile_number):
        self._mobile_number = mobile_number

    def get_mobile_number(self):
        return self._mobile_number

    def set_client_callback_url(self, callback_url):
        if not self._transaction:
            self._client_callback_url = callback_url
        else:
            raise ValidationError(
                'Transaction is already issued. Can not set callback url.'
            )

    def _get_verification_inputs(self, data):
        serializer = self._verification_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _set_reference_number(self, reference_number):
        self._reference_number = reference_number

    def get_reference_number(self):
        return self._reference_number

    def _set_transaction_status_text(self, txt):
        self._transaction_status_text = txt

    def get_transaction_status_text(self):
        return self._transaction_status_text

    def _set_payment_status(self, payment_status):
        if (
                payment_status == Transaction.StatusChoice.RETURN_FROM_BANK.value
                and self._transaction.status != Transaction.StatusChoice.REDIRECT_TO_BANK.value
        ):
            raise ValidationError(
                _(
                    'Changing transaction status is not possible in '
                    'current status which is [{status}].'
                ).format(status=Transaction.StatusChoice(self._transaction.status))
            )

        transaction_services.update_transaction(self._transaction, status=payment_status)
        self._transaction.refresh_from_db()

    def set_gateway_currency(self, currency):
        if currency not in CurrencyChoice:
            raise ValidationError(f'Gateway currency [{currency}] is not supported.')
        self._gateway_currency = currency

    def get_gateway_currency(self):
        return self._gateway_currency

    def set_currency(self, currency):
        if currency not in CurrencyChoice:
            raise ValidationError(f'Currency [{currency}] is not supported.')
        self._currency = currency

    def get_currency(self):
        return self._currency

    def get_gateway_amount(self):
        return self._gateway_amount

    def _set_tracking_code(self, tracking_code):
        self._tracking_code = tracking_code

    def get_tracking_code(self):
        return self._tracking_code

    def set_paying_user(self, paying_user):
        self._paying_user = paying_user

    def get_paying_user(self):
        return self._paying_user

    def redirect_gateway(self):
        if (timezone.now() - self._transaction.created_time).seconds > 120:
            self._set_payment_status(Transaction.StatusChoice.GATEWAY_TOKEN_EXPIRED.value)
            raise ValidationError()
        self._set_payment_status(Transaction.StatusChoice.REDIRECT_TO_BANK.value)
        return self.get_gateway_payment_url()

    def _get_gateway_callback_url(self):
        url = reverse(settings.CALLBACK_NAMESPACE)
        url_parts = list(parse.urlparse(url))
        if not (url_parts[0] and url_parts[1]):
            url = get_absolute_url(url)

        query = dict(
            bank_type=self._GATEWAY_SLUG,
            callback=base64_encode(self._client_callback_url),
            platform=self.get_platform()
        )
        return append_querystring(url, query)

    def _get_error_messages(self, value):
        return self._error_messages.get(value, 'Unknown error')

    @classmethod
    def get_minimum_amount(cls):
        return cls._MIN_AMOUNT

    @property
    def transaction(self):
        return self._transaction
