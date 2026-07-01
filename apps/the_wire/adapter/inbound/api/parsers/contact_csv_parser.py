import csv
import io

from fastapi import UploadFile
from the_wire.app.dtos.contact_dto import SaveContactCommand

_GOOGLE_EMAIL_COLS = ("E-mail 1 - Value", "E-mail 2 - Value")


def _extract_name(row: dict[str, str]) -> str:
    # 단순 포맷
    simple = (row.get("name") or row.get("이름") or "").strip()
    if simple:
        return simple
    # 구글 CSV 포맷
    parts = [
        row.get("Name Prefix", ""),
        row.get("First Name", ""),
        row.get("Middle Name", ""),
        row.get("Last Name", ""),
        row.get("Name Suffix", ""),
    ]
    google = " ".join(p.strip() for p in parts if p.strip())
    if google:
        return google
    return (row.get("Nickname") or row.get("File As") or "").strip()


def _extract_email(row: dict[str, str]) -> str:
    # 단순 포맷
    simple = (row.get("email") or row.get("이메일") or "").strip()
    if simple and "@" in simple:
        return simple
    # 구글 CSV 포맷
    for col in _GOOGLE_EMAIL_COLS:
        val = row.get(col, "").strip()
        if val and "@" in val:
            return val
    return ""


async def parse_contact_csv(file: UploadFile) -> list[SaveContactCommand]:
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    commands: list[SaveContactCommand] = []
    for row in reader:
        name = _extract_name(row)
        email = _extract_email(row)
        if name and email:
            commands.append(SaveContactCommand(name=name, email=email))
    return commands
