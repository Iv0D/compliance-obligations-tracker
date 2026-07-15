# DECISIONS.md

Documento para la defensa técnica. El detalle cronológico de cada decisión está en `registro-decisiones.md`.

## Arquitectura

### Backend (capas)

```
interfaces/http  →  application/use_cases  →  domain
                         ↓
                  infrastructure/repositories  →  Postgres
```

- **Dominio** (`domain/`): entidades, value objects, servicios puros (state machine, overdue, masking). Sin imports de FastAPI ni SQLAlchemy.
- **Application** (`application/`): un use case por operación; ports como Protocols para repos.
- **Infrastructure** (`infrastructure/`): modelos ORM, repos Postgres, optimistic lock en el `UPDATE`.
- **Interfaces** (`interfaces/http/`): rutas, schemas Pydantic, mappers, modelo de error. Sin reglas de negocio.

**Alternativa descartada:** controllers + service layer genérico + unit-of-work. Más capas sin beneficio en un scope chico.

### Frontend (features)

- **Server Components** para lecturas (dashboard, detalle).
- **Server Actions** para mutaciones (crear, editar, cambiar estado, borrar).
- **`features/obligations/api.ts`**: cliente HTTP; no replica reglas de dominio.
- **`valid_transitions` y `can_submit` vienen del backend**; el front solo renderiza y deshabilita botones.

**Alternativa descartada:** next-intl u otra librería i18n. Diccionario propio mínimo (decisión 016).

### Qué dejé afuera a propósito

- Autenticación y roles.
- CI/CD, deploy a producción.
- Upload real de documentos (mock con `filename` + `mock_url`).
- Paginación, búsqueda, recordatorios por email.
- Migraciones formales (Alembic); uso `create_all()` al arrancar.
- Controllers HTTP separados de las rutas.

---

## Contrato de API

OpenAPI en `/docs`. Resumen:

| Método | Ruta | Body clave | Respuesta |
|--------|------|------------|-----------|
| `GET` | `/dashboard` | — | KPIs |
| `GET` | `/obligations?status=` | — | lista (taxId enmascarado) |
| `POST` | `/obligations` | type, title, owner, due_date, company_tax_id | detalle |
| `GET` | `/obligations/{id}` | — | detalle + audit + valid_transitions + can_submit |
| `PUT` | `/obligations/{id}` | campos + **version** | detalle |
| `DELETE` | `/obligations/{id}` | — | 204 |
| `PATCH` | `/obligations/{id}/status` | status + **version** | detalle |
| `POST` | `/obligations/{id}/documents` | filename, mock_url | documento |

**Errores** (todas las rutas): `{"error": {"code": "...", "message": "..."}}`

| code | HTTP |
|------|------|
| `not_found` | 404 |
| `conflict` | 409 |
| `invalid_transition` | 422 |
| `document_required` | 422 |
| `invalid_company_tax_id` | 422 |
| `validation_error` | 422 |

---

## Overdue

- **Dónde vive:** `domain/services/overdue.py`.
- **Regla:** `due_date < today` y status no es `submitted` ni `done`.
- **No se persiste** como estado ni columna; se calcula en listado y detalle.
- **Próximas a vencer (KPI):** ventana de 7 días, excluyendo vencidas y terminales (decisión 010).

---

## Concurrencia

- **Estrategia:** optimistic locking con campo `version`.
- **Dónde:** el repo incrementa `version` en un solo `UPDATE ... WHERE version = expected`; si `rowcount == 0` → `ConcurrencyConflictError` → HTTP 409.
- **Cliente envía** `version` en body de `PUT` y `PATCH /status`.
- **Alternativa descartada:** header `If-Match` (más estándar REST, pero más fricción para el front en este scope).

---

## Dato sensible (`companyTaxId`)

- **Persistencia:** valor completo en DB.
- **Lecturas API:** solo `company_tax_id_masked` (`••••6789`); el campo crudo nunca se serializa.
- **Logs:** `change_status` loguea id y estados, nunca el taxId; test de integración lo verifica.
- **Soft delete:** se marca `deleted_at` y se vacía `company_tax_id` en el mismo UPDATE (decisión 023).
- **Edición:** el usuario debe reingresar el taxId completo; no se puede enviar el valor enmascarado (decisión 021).

---

## Uso de IA (Cursor)

Usé IA para scaffolding, tests y acelerar implementación. **No acepté output sin revisar.** Ejemplos concretos donde corregí o rechacé:

1. **TaxId en edición:** el formulario enviaba el valor enmascarado al backend si el campo quedaba vacío, lo que hubiera corrompido el dato. Rechacé el fallback; el taxId es obligatorio al editar y se muestra el enmascarado solo como referencia.

2. **Version duplicada en `ChangeStatusUseCase`:** la IA incrementaba `version` en el use case y también en el repo. Quité el incremento manual del use case; solo el repo lo hace atómicamente en el `UPDATE`.

3. **Soft delete vs hard delete:** la IA sugirió hard delete para alinear con el ER. Elegí soft delete + anonimizar taxId para conservar audit trail sin dejar el dato sensible en filas borradas.

4. **Helper `_latest_created` en rutas:** generaba el detalle buscando la última fila creada. Lo reemplacé por retornar la obligación que ya devuelve el use case de creación.

El log completo de decisiones y correcciones está en `registro-decisiones.md`.
