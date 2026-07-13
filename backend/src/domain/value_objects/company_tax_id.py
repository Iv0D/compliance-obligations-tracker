from dataclasses import dataclass

from src.domain.errors.domain_errors import InvalidCompanyTaxIdError

_MASK = "••••"


@dataclass(frozen=True)
class CompanyTaxId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise InvalidCompanyTaxIdError("company_tax_id must not be empty")

    def masked(self) -> str:
        return f"{_MASK}{self.value[-4:]}"
