# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class AuthenticationCodeType(BaseObject):
    """
    Provides information about the method by which an authentication code is delivered to the user
    
    """

    ID: str = Field("authenticationCodeType", alias="@type")


class AuthenticationCodeTypeCall(AuthenticationCodeType):
    """
    An authentication code is delivered via a phone call to the specified phone number
    
    :param length: Length of the code
    :type length: :class:`int`
    
    """

    ID: str = Field("authenticationCodeTypeCall", alias="@type")
    length: int

    @staticmethod
    def read(q: dict) -> AuthenticationCodeTypeCall:
        return AuthenticationCodeTypeCall.construct(**q)


class AuthenticationCodeTypeFlashCall(AuthenticationCodeType):
    """
    An authentication code is delivered by an immediately canceled call to the specified phone number. The number from which the call was made is the code
    
    :param pattern: Pattern of the phone number from which the call will be made
    :type pattern: :class:`str`
    
    """

    ID: str = Field("authenticationCodeTypeFlashCall", alias="@type")
    pattern: str

    @staticmethod
    def read(q: dict) -> AuthenticationCodeTypeFlashCall:
        return AuthenticationCodeTypeFlashCall.construct(**q)


class AuthenticationCodeTypeSms(AuthenticationCodeType):
    """
    An authentication code is delivered via an SMS message to the specified phone number
    
    :param length: Length of the code
    :type length: :class:`int`
    
    """

    ID: str = Field("authenticationCodeTypeSms", alias="@type")
    length: int

    @staticmethod
    def read(q: dict) -> AuthenticationCodeTypeSms:
        return AuthenticationCodeTypeSms.construct(**q)


class AuthenticationCodeTypeTelegramMessage(AuthenticationCodeType):
    """
    An authentication code is delivered via a private Telegram message, which can be viewed from another active session
    
    :param length: Length of the code
    :type length: :class:`int`
    
    """

    ID: str = Field("authenticationCodeTypeTelegramMessage", alias="@type")
    length: int

    @staticmethod
    def read(q: dict) -> AuthenticationCodeTypeTelegramMessage:
        return AuthenticationCodeTypeTelegramMessage.construct(**q)
