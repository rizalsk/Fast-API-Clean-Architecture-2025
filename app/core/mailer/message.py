from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from app.dependencies.logger import log

class Message:
    def __init__(self, template_dir: str = "emails"):
        self.to_email = None
        self.subject_text = None
        self.html_template = None
        self.context = {}
        self.text_body = None

        parent_dir = Path(__file__).resolve().parent.parent.parent / "views"
        template_path = parent_dir / template_dir
        template_path = template_path.resolve()

        log.info(f"Template folder: {template_path}")

        if template_path.exists() and template_path.is_dir():
            self.env = Environment(loader=FileSystemLoader(str(template_path)))
        else:
            log.warning(f"Template folder '{template_path}' tidak ditemukan, menggunakan loader kosong")
            self.env = Environment(loader=FileSystemLoader([]))

    def to(self, email: str):
        self.to_email = email
        return self

    def subject(self, text: str):
        self.subject_text = text
        return self

    def template(self, file: str, context: dict = {}):
        self.html_template = file
        self.context = context
        return self

    def text(self, content: str):
        self.text_body = content
        return self

    def build_html(self):
        if not self.html_template:
            return None

        template = self.env.get_template(self.html_template)
        return template.render(**self.context)
