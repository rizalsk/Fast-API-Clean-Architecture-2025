from fastapi import APIRouter, Depends, Form, UploadFile, File
from app.schemas.email import SendEmailSchema
from app.dependencies.auth import get_current_user_id
from core.mailer.mail import Mail
from typing import Optional, List
from app.services.file_service import UPLOAD_DIR
import shutil

email_router = APIRouter(prefix="/v1/email-test", tags=["Email-test"])

@email_router.post("/send-text")
def send_text_email(data: SendEmailSchema, user_id: int = Depends(get_current_user_id)):
    return Mail.to(data.to) \
        .subject(data.subject) \
        .text(
            "Text email\n"
            "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\n"
            "fugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\n"
            "qui aperiam non debitis possimus qui neque nisi nulla"
        ).send()

@email_router.post("/send-template")
def send_template_email(data: SendEmailSchema, user_id: int = Depends(get_current_user_id)):
    return Mail.to(data.to) \
        .subject(data.subject) \
        .template("welcome.html", {"name": "John Doe"}) \
        .send()


@email_router.post("/send-attachment")
def send_attachment_email(data: SendEmailSchema, user_id: int = Depends(get_current_user_id)):
    return Mail.to(data.to)\
            .subject("Welcome Email")\
            .template("welcome.html", {"name": "John Doe"})\
            .attach("app/assets/uploads/7f33cb5f-38a2-4cc4-b4ff-e5883173fe3c_bg-img5.jpg")\
            .send()

@email_router.post("/send-attachment-upload")
async def send_text_email(
    to: str = Form(...),
    subject: str = Form(...),
    body: str = Form(...),
    attachments: Optional[List[UploadFile]] = File(None),
    user_id: int = Depends(get_current_user_id)
):
    # Simpan file sementara
    attachments = []
    if attachments:
        for file in attachments:
            dest = UPLOAD_DIR / file.filename
            with open(dest, "wb") as f:
                shutil.copyfileobj(file.file, f)
            attachments.append(str(dest))

    mail = Mail.to(to).subject(subject).text(body)
    for file_path in attachments:
        mail.attach(file_path)
    return mail.send()
