import logging

from sqlmodel import delete

from titanic.adapter.outbound.orm.titanic_passenger_orm import TitanicPassengerOrm
from titanic.app.dtos.james_dto import BookingCommand, PersonCommand
from titanic.app.ports.output.james_repository_port import JamesRepositoryPort
from titanic.app.titanic_flow_log import titanic_flow_log

logger = logging.getLogger(__name__)


class JamesPgRepository(JamesRepositoryPort):
    db = None

    @staticmethod
    async def receive_uploaded_records(
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        print("[제임스 레포지터리] PersonCommand 상위 5개 레코드:")
        for person in person_commands[:5]:
            print(
                "PersonCommand("
                f"passenger_id='{person.passenger_id}', "
                f"name='{person.name}', "
                f"gender='{person.gender}', "
                f"age='{person.age}', "
                f"sib_sp='{person.sib_sp}', "
                f"parch='{person.parch}', "
                f"survived='{person.survived}'"
                ")"
            )

        print("[제임스 레포지터리] BookingCommand 상위 5개 레코드:")
        for booking in booking_commands[:5]:
            print(
                "BookingCommand("
                f"pclass='{booking.pclass}', "
                f"ticket='{booking.ticket}', "
                f"fare='{booking.fare}', "
                f"cabin='{booking.cabin}', "
                f"embarked='{booking.embarked}'"
                ")"
            )

        orm_rows = [
            TitanicPassengerOrm.from_passenger_row(
                "Titanic-Dataset.csv",
                person.to_passenger_row(),
            )
            for person in person_commands
        ]
        logger.info(
            "[제임스 레포지터리] 저장 시작 file=%s rows=%s",
            "Titanic-Dataset.csv",
            len(orm_rows),
        )

        titanic_flow_log(
            "james-upload",
            "outbound",
            "Neon replace rows=%s",
            len(orm_rows),
            source_file="Titanic-Dataset.csv",
        )

        await JamesPgRepository.db.execute(delete(TitanicPassengerOrm))
        JamesPgRepository.db.add_all(orm_rows)
        await JamesPgRepository.db.commit()
        logger.info(
            "[제임스 레포지터리] 저장 완료 file=%s rows=%s",
            "Titanic-Dataset.csv",
            len(orm_rows),
        )

        return len(orm_rows)