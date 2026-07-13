from datetime import date

from pydantic import BaseModel, Field

from src.application.dtos.obligation_dto import (
    CreateObligationInput,
    UpdateObligationInput,
)
from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus


class CreateObligationRequest(BaseModel):
    type: ObligationType
    title: str = Field(min_length=1, max_length=255)
    owner: str = Field(min_length=1, max_length=255)
    due_date: date
    company_tax_id: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=2000)
    requires_document: bool = False

    def to_input(self) -> CreateObligationInput:
        return CreateObligationInput(
            type=self.type,
            title=self.title,
            owner=self.owner,
            due_date=self.due_date,
            company_tax_id=self.company_tax_id,
            description=self.description,
            requires_document=self.requires_document,
        )


class UpdateObligationRequest(BaseModel):
    type: ObligationType
    title: str = Field(min_length=1, max_length=255)
    owner: str = Field(min_length=1, max_length=255)
    due_date: date
    company_tax_id: str = Field(min_length=1, max_length=50)
    version: int = Field(ge=1)
    description: str | None = Field(default=None, max_length=2000)
    requires_document: bool = False

    def to_input(self) -> UpdateObligationInput:
        return UpdateObligationInput(
            type=self.type,
            title=self.title,
            owner=self.owner,
            due_date=self.due_date,
            company_tax_id=self.company_tax_id,
            description=self.description,
            requires_document=self.requires_document,
        )


class ChangeStatusRequest(BaseModel):
    status: ObligationStatus
    version: int = Field(ge=1)


class AttachDocumentRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    mock_url: str = Field(min_length=1, max_length=1024)
