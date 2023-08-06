# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject


class DeleteChatMessagesFromUser(BaseObject):
    """
    Deletes all messages sent by the specified user to a chat. Supported only for supergroups; requires can_delete_messages administrator privileges
    
    :param chat_id: Chat identifier
    :type chat_id: :class:`int`
    
    :param user_id: User identifier
    :type user_id: :class:`int`
    
    """

    ID: str = Field("deleteChatMessagesFromUser", alias="@type")
    chat_id: int
    user_id: int

    @staticmethod
    def read(q: dict) -> DeleteChatMessagesFromUser:
        return DeleteChatMessagesFromUser.construct(**q)
