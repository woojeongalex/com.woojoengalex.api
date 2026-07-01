import csv
import io

from fastapi import UploadFile
from the_wire.app.dtos.contact_dto import SaveContactCommand


async def parse_contact_csv(file: UploadFile) -> list[SaveContactCommand]:
    content = await file.read()
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    commands: list[SaveContactCommand] = []
    for row in reader:
        name = (row.get("name") or row.get("이름") or "").strip()
        email = (row.get("email") or row.get("이메일") or "").strip()
        if name and email and "@" in email:
            commands.append(SaveContactCommand(name=name, email=email))
    return commands
