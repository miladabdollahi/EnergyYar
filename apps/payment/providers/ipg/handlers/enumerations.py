from django.db.models import TextChoices


class MellatResponseChoice(TextChoices):
    SUCCESS = ('0', 'Transaction was successful')
    INVALID_CARD_NUMBER = ('11', 'Invalid card number')
    INSUFFICIENT_BALANCE = ('12', 'Insufficient balance')
    INCORRECT_PASSWORD = ('13', 'The password is incorrect')
    TOO_MANY_INCORRECT_PASSWORDS = ('14', 'Too many attempts with incorrect password')
    INVALID_CARD = ('15', 'Invalid card')
    TOO_MANY_WITHDRAWAL = ('16', 'Too many withdrawal operations')
    USER_CANCELED = ('17', 'User has canceled the transaction')
    CARD_EXPIRED = ('18', 'Card has been expired')
    WITHDRAW_LIMIT_REACHED = ('19', 'Withdrawal amount is above the limit')
    INVALID_CARD_ISSUER = ('111', 'Card issuer is invalid')
    SWITCH_ERROR = ('112', 'Card issuer switch error')
    NO_RESPONSE_FROM_CARD_ISSUER = ('113', 'No response from card issuer')
    TRANSACTION_NOT_ALLOWED = ('114', 'Card holder is not allowed to perform this transaction')
    INVALID_ACCEPTOR = ('21', 'Invalid acceptor')
    SECURITY_ERROR = ('23', 'Security error')
    INVALID_ACCEPTOR_INFO = ('24', 'Acceptor info is invalid')
    INVALID_AMOUNT = ('25', 'Invalid amount')
    INVALID_RESPONSE = ('31', 'Invalid response')
    INVALID_INPUT_FORMAT = ('32', 'Invalid input data format')
    INVALID_ACCOUNT = ('33', 'Invalid account')
    SYSTEM_ERROR = ('34', 'Internal system error')
    INVALID_DATE = ('35', 'Invalid date')
    DUPLICATE_SALE_ORDER_ID = ('41', 'SaleOrderId is duplicate')
    SALE_TRANSACTION_NOT_FOUND = ('42', 'Sale transaction not found')
    TRANSACTION_ALREADY_VERIFIED = ('43', 'Transaction has been already verified')
    VERIFY_REQUEST_NOT_FOUND = ('44', 'Verify request not found')
    TRANSACTION_ALREADY_SETTLED = ('45', 'Transaction has been already settled')
    TRANSACTION_NOT_SETTLED = ('46', 'Transaction has not been settled')
    SETTLE_TRANSACTION_NOT_FOUND = ('47', 'Settle transaction not found')
    TRANSACTION_ALREADY_REVERSED = ('48', 'Transaction has been already reversed')
    INCORRECT_BILLING_ID = ('412', 'Billing ID is incorrect')
    INCORRECT_PAYMENT_CODE = ('413', 'Payment code is incorrect')
    INVALID_BILL_ISSUER = ('414', 'Bill issuing organization is invalid')
    SESSION_EXPIRED = ('415', 'Session has expired')
    DATA_SUBMISSION_ERROR = ('416', 'Data submission error')
    INVALID_PAYER_ID = ('417', 'Invalid Payer ID')
    CUSTOMER_INFO_ERROR = ('418', 'Error defining customer info')
    TOO_MANY_DATA_INPUTS = ('419', 'Too many attempts for data input')
    INVALID_IP = ('421', 'Acceptor IP is not valid')
    DUPLICATE_TRANSACTION = ('51', 'Transaction is duplicate')
    REFERENCE_TRANSACTION_NOT_FOUND = ('54', 'Reference transaction not found')
    INVALID_TRANSACTION = ('55', 'Invalid transaction')
    DEPOSIT_ERROR = ('61', 'Deposit error')
    INVALID_CALLBACK_URL = ('62', 'Acceptor callback url is not valid')
    STATIC_PASSWORD_LIMIT_REACHED = ('98', 'Static password usage limit has been reached')

    @classmethod
    def failure(cls):
        return cls.INVALID_CARD_NUMBER, cls.INSUFFICIENT_BALANCE, cls.INCORRECT_PASSWORD, \
            cls.TOO_MANY_INCORRECT_PASSWORDS, cls.INVALID_CARD, cls.TOO_MANY_WITHDRAWAL, \
            cls.CARD_EXPIRED, cls.WITHDRAW_LIMIT_REACHED, cls.INVALID_CARD_ISSUER, \
            cls.SWITCH_ERROR, cls.NO_RESPONSE_FROM_CARD_ISSUER, cls.TRANSACTION_NOT_ALLOWED, \
            cls.INVALID_ACCEPTOR, cls.SECURITY_ERROR, cls.INVALID_ACCEPTOR_INFO, \
            cls.INVALID_AMOUNT, cls.INVALID_RESPONSE, cls.INVALID_INPUT_FORMAT, \
            cls.INVALID_ACCOUNT, cls.SYSTEM_ERROR, cls.INVALID_DATE, \
            cls.DUPLICATE_SALE_ORDER_ID, cls.SALE_TRANSACTION_NOT_FOUND, \
            cls.VERIFY_REQUEST_NOT_FOUND, cls.TRANSACTION_NOT_SETTLED, \
            cls.SETTLE_TRANSACTION_NOT_FOUND, cls.INCORRECT_BILLING_ID, \
            cls.INCORRECT_PAYMENT_CODE, cls.INVALID_BILL_ISSUER, cls.DATA_SUBMISSION_ERROR, \
            cls.INVALID_PAYER_ID, cls.CUSTOMER_INFO_ERROR, cls.TOO_MANY_DATA_INPUTS, \
            cls.INVALID_IP, cls.DUPLICATE_TRANSACTION, cls.REFERENCE_TRANSACTION_NOT_FOUND, \
            cls.INVALID_TRANSACTION, cls.DEPOSIT_ERROR, cls.INVALID_CALLBACK_URL, \
            cls.STATIC_PASSWORD_LIMIT_REACHED

    @classmethod
    def already_done(cls):
        return cls.TRANSACTION_ALREADY_VERIFIED, cls.TRANSACTION_ALREADY_SETTLED, \
            cls.TRANSACTION_ALREADY_REVERSED

    @classmethod
    def canceled(cls):
        return cls.USER_CANCELED, cls.SESSION_EXPIRED


class PasargadResponseChoice(TextChoices):
    SUCCESS = ('0', 'Transaction was successful')
    INVALID_CARD_NUMBER = ('11', 'Invalid card number')
    INSUFFICIENT_BALANCE = ('12', 'Insufficient balance')
    INCORRECT_PASSWORD = ('13', 'The password is incorrect')
    TOO_MANY_INCORRECT_PASSWORDS = ('14', 'Too many attempts with incorrect password')
    INVALID_CARD = ('15', 'Invalid card')
    TOO_MANY_WITHDRAWAL = ('16', 'Too many withdrawal operations')
    USER_CANCELED = ('17', 'User has canceled the transaction')
    CARD_EXPIRED = ('18', 'Card has been expired')
    WITHDRAW_LIMIT_REACHED = ('19', 'Withdrawal amount is above the limit')
    INVALID_CARD_ISSUER = ('111', 'Card issuer is invalid')
    SWITCH_ERROR = ('112', 'Card issuer switch error')
    NO_RESPONSE_FROM_CARD_ISSUER = ('113', 'No response from card issuer')
    TRANSACTION_NOT_ALLOWED = ('114', 'Card holder is not allowed to perform this transaction')
    INVALID_ACCEPTOR = ('21', 'Invalid acceptor')
    SECURITY_ERROR = ('23', 'Security error')
    INVALID_ACCEPTOR_INFO = ('24', 'Acceptor info is invalid')
    INVALID_AMOUNT = ('25', 'Invalid amount')
    INVALID_RESPONSE = ('31', 'Invalid response')
    INVALID_INPUT_FORMAT = ('32', 'Invalid input data format')
    INVALID_ACCOUNT = ('33', 'Invalid account')
    SYSTEM_ERROR = ('34', 'Internal system error')
    INVALID_DATE = ('35', 'Invalid date')
    DUPLICATE_SALE_ORDER_ID = ('41', 'SaleOrderId is duplicate')
    SALE_TRANSACTION_NOT_FOUND = ('42', 'Sale transaction not found')
    TRANSACTION_ALREADY_VERIFIED = ('43', 'Transaction has been already verified')
    VERIFY_REQUEST_NOT_FOUND = ('44', 'Verify request not found')
    TRANSACTION_ALREADY_SETTLED = ('45', 'Transaction has been already settled')
    TRANSACTION_NOT_SETTLED = ('46', 'Transaction has not been settled')
    SETTLE_TRANSACTION_NOT_FOUND = ('47', 'Settle transaction not found')
    TRANSACTION_ALREADY_REVERSED = ('48', 'Transaction has been already reversed')
    INCORRECT_BILLING_ID = ('412', 'Billing ID is incorrect')
    INCORRECT_PAYMENT_CODE = ('413', 'Payment code is incorrect')
    INVALID_BILL_ISSUER = ('414', 'Bill issuing organization is invalid')
    SESSION_EXPIRED = ('415', 'Session has expired')
    DATA_SUBMISSION_ERROR = ('416', 'Data submission error')
    INVALID_PAYER_ID = ('417', 'Invalid Payer ID')
    CUSTOMER_INFO_ERROR = ('418', 'Error defining customer info')
    TOO_MANY_DATA_INPUTS = ('419', 'Too many attempts for data input')
    INVALID_IP = ('421', 'Acceptor IP is not valid')
    DUPLICATE_TRANSACTION = ('51', 'Transaction is duplicate')
    REFERENCE_TRANSACTION_NOT_FOUND = ('54', 'Reference transaction not found')
    INVALID_TRANSACTION = ('55', 'Invalid transaction')
    DEPOSIT_ERROR = ('61', 'Deposit error')
    INVALID_CALLBACK_URL = ('62', 'Acceptor callback url is not valid')
    STATIC_PASSWORD_LIMIT_REACHED = ('98', 'Static password usage limit has been reached')

    @classmethod
    def failure(cls):
        return cls.INVALID_CARD_NUMBER, cls.INSUFFICIENT_BALANCE, cls.INCORRECT_PASSWORD, \
            cls.TOO_MANY_INCORRECT_PASSWORDS, cls.INVALID_CARD, cls.TOO_MANY_WITHDRAWAL, \
            cls.CARD_EXPIRED, cls.WITHDRAW_LIMIT_REACHED, cls.INVALID_CARD_ISSUER, \
            cls.SWITCH_ERROR, cls.NO_RESPONSE_FROM_CARD_ISSUER, cls.TRANSACTION_NOT_ALLOWED, \
            cls.INVALID_ACCEPTOR, cls.SECURITY_ERROR, cls.INVALID_ACCEPTOR_INFO, \
            cls.INVALID_AMOUNT, cls.INVALID_RESPONSE, cls.INVALID_INPUT_FORMAT, \
            cls.INVALID_ACCOUNT, cls.SYSTEM_ERROR, cls.INVALID_DATE, \
            cls.DUPLICATE_SALE_ORDER_ID, cls.SALE_TRANSACTION_NOT_FOUND, \
            cls.VERIFY_REQUEST_NOT_FOUND, cls.TRANSACTION_NOT_SETTLED, \
            cls.SETTLE_TRANSACTION_NOT_FOUND, cls.INCORRECT_BILLING_ID, \
            cls.INCORRECT_PAYMENT_CODE, cls.INVALID_BILL_ISSUER, cls.DATA_SUBMISSION_ERROR, \
            cls.INVALID_PAYER_ID, cls.CUSTOMER_INFO_ERROR, cls.TOO_MANY_DATA_INPUTS, \
            cls.INVALID_IP, cls.DUPLICATE_TRANSACTION, cls.REFERENCE_TRANSACTION_NOT_FOUND, \
            cls.INVALID_TRANSACTION, cls.DEPOSIT_ERROR, cls.INVALID_CALLBACK_URL, \
            cls.STATIC_PASSWORD_LIMIT_REACHED

    @classmethod
    def already_done(cls):
        return cls.TRANSACTION_ALREADY_VERIFIED, cls.TRANSACTION_ALREADY_SETTLED, \
            cls.TRANSACTION_ALREADY_REVERSED

    @classmethod
    def canceled(cls):
        return cls.USER_CANCELED, cls.SESSION_EXPIRED
