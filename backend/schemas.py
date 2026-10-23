from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator

class Message(BaseModel):
    role: Literal['user', 'assistant']
    content: str = Field(min_length=1, max_length=12000)
    @field_validator('content')
    @classmethod
    def valid_content(cls, value):
        if not value.strip():
            raise ValueError('Pesan tidak boleh kosong.')
        return value

class ChatRequest(BaseModel):
    worker_id: str = Field(min_length=1, max_length=40)
    messages: list[Message] = Field(min_length=1, max_length=30)
    @model_validator(mode='after')
    def valid_history(self):
        if self.messages[-1].role != 'user':
            raise ValueError('Pesan terakhir harus dari pengguna.')
        if any(len(m.content) > 4000 for m in self.messages if m.role == 'user'):
            raise ValueError('Pesan pengguna maksimal 4000 karakter.')
        if sum(len(m.content) for m in self.messages) > 60000:
            raise ValueError('Riwayat terlalu panjang.')
        return self
