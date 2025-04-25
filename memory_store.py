from langchain.memory import ConversationBufferWindowMemory
from constant import MEMORY_WINDOW_SIZE

class MemoryStore:
    def __init__(self):
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=MEMORY_WINDOW_SIZE,
            return_messages=True
        )
    
    def get_memory(self):
        return self.memory
    
    def clear_memory(self):
        self.memory.clear()
