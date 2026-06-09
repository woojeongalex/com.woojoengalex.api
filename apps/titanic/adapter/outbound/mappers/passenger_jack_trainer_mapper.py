from titanic.adapter.outbound.orm.passenger_orm import PersonOrm
from titanic.domain.entities.passenger_jack_trainer_entity import TitanicPassenger
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelations,
    Gender,
    PassengerId,
    PassengerName,
)


def orm_to_entity(orm: PersonOrm) -> TitanicPassenger:
    entity = TitanicPassenger(
        id=orm.id,
        passenger_id=PassengerId(int(orm.passenger_id)) if orm.passenger_id else None,
        name=PassengerName(orm.name),
        gender=Gender.from_str(orm.gender),
        age=Age(float(orm.age) if orm.age else None),
        family=FamilyRelations(
            sib_sp=int(orm.sib_sp) if orm.sib_sp else 0,
            parch=int(orm.parch) if orm.parch else 0,
        ),
        _survived="unknown",
    )
    survived_code = int(orm.survived) if orm.survived in ("0", "1") else None
    entity.record_survival_result(survived_code)
    return entity


def entity_to_orm(entity: TitanicPassenger, source_file: str = "") -> PersonOrm:
    return PersonOrm(
        id=entity.id,
        source_file=source_file,
        passenger_id=str(entity.passenger_id.value) if entity.passenger_id else "",
        survived="1" if entity.survived_status == "survived" else "0" if entity.survived_status == "perished" else "",
        name=entity.name.value,
        gender=entity.gender.value,
        age=str(entity.age.value) if not entity.age.is_missing else "",
        sib_sp=str(entity.family.sib_sp),
        parch=str(entity.family.parch),
    )
