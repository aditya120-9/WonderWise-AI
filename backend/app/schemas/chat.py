from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
	message: str = Field(..., min_length=1, max_length=4000)
	conversation_id: int = Field(default=1, ge=1)

	@field_validator("message")
	@classmethod
	def message_must_contain_text(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("message must contain non-whitespace text")
		return value
