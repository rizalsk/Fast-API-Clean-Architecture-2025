from pydantic import BaseModel, EmailStr

class SendEmailSchema(BaseModel):
    to: EmailStr
    subject: str