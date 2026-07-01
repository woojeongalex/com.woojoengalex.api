import csv
import io

from fastapi import UploadFile
from the_wire.app.dtos.contact_dto import SaveContactCommand

_EMAIL_COLS = ("E-mail 1 - Value", "E-mail 2 - Value")


def _build_name(row: dict[str, str]) -> str:
    parts = [
        row.get("Name Prefix", ""),
        row.get("First Name", ""),
        row.get("Middle Name", ""),
        row.get("Last Name", ""),
        row.get("Name Suffix", ""),
    ]
    name = " ".join(p.strip() for p in parts if p.strip())
    if not name:
        name = (row.get("Nickname") or row.get("File As") or "").strip()
    return name


def _pick_email(row: dict[str, str]) -> str:
    for col in _EMAIL_COLS:
        val = row.get(col, "").strip()
        if val and "@" in val:
            return val
    return ""


async def parse_google_contacts_csv(file: UploadFile) -> list[SaveContactCommand]:
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    commands: list[SaveContactCommand] = []
    for row in reader:
        name = _build_name(row)
        email = _pick_email(row)
        if name and email:
            commands.append(SaveContactCommand(name=name, email=email))
    return commands
