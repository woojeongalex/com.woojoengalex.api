from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from the_wire.adapter.outbound.orm.contact_model import ContactModel
from the_wire.app.dtos.contact_dto import (
    ContactResult,
    SaveContactCommand,
    SearchContactQuery,
)
from the_wire.app.ports.output.contact_repository_port import ContactRepositoryPort


class ContactPgRepository(ContactRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, command: SaveContactCommand) -> ContactResult:
        stmt = (
            insert(ContactModel)
            .values(name=command.name, email=command.email)
            .on_conflict_do_update(
                index_elements=["email"],
                set_={"name": command.name},
            )
            .returning(ContactModel.name, ContactModel.email)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        row = result.one()
        return ContactResult(name=row.name, email=row.email)

    async def search(self, query: SearchContactQuery) -> list[ContactResult]:
        stmt = (
            select(ContactModel).where(ContactModel.name.ilike(f"%{query.q}%")).limit(5)
        )
        result = await self._session.execute(stmt)
        return [
            ContactResult(name=row.name, email=row.email) for row in result.scalars()
        ]

    async def list_all(self) -> list[ContactResult]:
        stmt = select(ContactModel).order_by(ContactModel.name)
        result = await self._session.execute(stmt)
        return [
            ContactResult(name=row.name, email=row.email) for row in result.scalars()
        ]
