from src.domain.value_objects.company_tax_id import CompanyTaxId


def redact_tax_id(text: str, raw_tax_id: str) -> str:
    if not raw_tax_id or not raw_tax_id.strip():
        return text
    return text.replace(raw_tax_id, CompanyTaxId(raw_tax_id).masked())
