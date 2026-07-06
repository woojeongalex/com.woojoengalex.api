from pydantic import BaseModel, ConfigDict, Field


class PubSubMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: str
    message_id: str = Field(alias="messageId")
    publish_time: str = Field(alias="publishTime")


class PubSubPushRequest(BaseModel):
    message: PubSubMessage
    subscription: str


class ReceiverAckResponse(BaseModel):
    status: str
