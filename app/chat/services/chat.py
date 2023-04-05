from app.chat.models.chat import Chat
from app.chat.repositories.chat import ChatRepository


class ChatService:
    def __init__(self):
        self.chat_repo = ChatRepository(Chat)
