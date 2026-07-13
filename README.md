# Compliance Obligations Tracker

Seguimiento de obligaciones de compliance de una empresa: qué presentar, cuándo vence, en qué estado y con qué documentación. Backend con reglas de dominio aisladas (máquina de estados, invariante doc-gated, overdue derivado, audit trail, dato sensible enmascarado, concurrencia con optimistic lock) y frontend Next.js con i18n es/en.

## Stack

- **Backend:** FastAPI + Pydantic + SQLAlchemy + PostgreSQL (SQLite en tests). Capas: `domain` → `application` → `infrastructure` + `interfaces/http`.
- **Frontend:** Next.js (App Router) + React + TS strict + Tailwind. Server Components por defecto, Server Actions para mutaciones. i18n propio (sin librería).

## Estructura

```
backend/src/
  domain/            reglas de negocio puras (sin HTTP, sin DB)
    entities/        Obligation, Document, AuditEvent
    value_objects/   Status, ObligationType, CompanyTaxId
    services/        state machine, overdue, tax id masking
    errors/          errores de dominio
  application/       casos de uso + ports (interfaces de repos) + DTOs
  infrastructure/    modelos SQLAlchemy, repos Postgres, session, logging
  interfaces/http/   rutas FastAPI, schemas, mappers, modelo de error
  config/            settings + logging
  main.py            entrypoint (create_app)

frontend/src/
  app/[locale]/            páginas (dashboard, detalle, crear, editar) + loading/error
  features/obligations/    api client, server actions, formulario
  components/              primitivas UI
  i18n/                    diccionarios es/en + provider
  lib/                     http-client + tipos
  middleware.ts            redirección de locale
```

## Modelo de datos (3 tablas)

| Tabla | Campos | Relación |
|-------|--------|----------|
| `obligations` | `id` · `type` · `title` · `description` · `status` · `due_date` · `owner` · `requires_document` · `company_tax_id` · `version` · `created_at` · `updated_at` · `deleted_at` | — |
| `documents` | `id` · `obligation_id` (FK) · `filename` · `mock_url` · `created_at` | una obligación **tiene** documentos |
| `audit_events` | `id` · `obligation_id` (FK) · `from_status` · `to_status` · `changed_at` | una obligación **registra** eventos |

`company_tax_id` se guarda completo, se expone enmascarado (`••••6789`) y nunca se loguea. Al hacer soft delete se marca `deleted_at` y se anonimiza `company_tax_id`, preservando el audit trail.

```mermaid
erDiagram
    OBLIGATION ||--o{ DOCUMENT : has
    OBLIGATION ||--o{ AUDIT_EVENT : records

    OBLIGATION {
        uuid id PK
        string type
        string title
        string description
        string status
        date due_date
        string owner
        boolean requires_document
        string company_tax_id
        int version
        datetime created_at
        datetime updated_at
        datetime deleted_at
    }

    DOCUMENT {
        uuid id PK
        uuid obligation_id FK
        string filename
        string mock_url
        datetime created_at
    }

    AUDIT_EVENT {
        uuid id PK
        uuid obligation_id FK
        string from_status
        string to_status
        datetime changed_at
    }
```

## Reglas de dominio (dónde viven)

| Regla | Ubicación |
|-------|-----------|
| Máquina de estados (`pending → in_progress → submitted → done` + rework/reopen) | `domain/value_objects/status.py` + `domain/services/state_machine.py` |
| Invariante doc-gated (no `submitted` sin documento si `requires_document`) | `domain/services/state_machine.py` |
| Overdue derivado (no es un estado guardado) | `domain/services/overdue.py` |
| Enmascarado del tax id | `domain/value_objects/company_tax_id.py` + `domain/services/tax_id_masking.py` |
| Audit trail (de→a + timestamp) | `application/use_cases/change_status.py` |
| Concurrencia (optimistic lock por `version`) | `infrastructure/repositories/postgres_obligation_repository.py` |

Ninguna regla vive en el handler HTTP: las rutas solo traducen HTTP ↔ use case ↔ DTO.

## API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health` | healthcheck |
| `GET` | `/dashboard` | KPIs (total, por estado, vencidas, próximas) |
| `GET` | `/obligations?status=` | listado (filtro opcional por estado) |
| `POST` | `/obligations` | crear |
| `GET` | `/obligations/{id}` | detalle (campos + audit + transiciones válidas + can_submit) |
| `PUT` | `/obligations/{id}` | editar (requiere `version`) |
| `DELETE` | `/obligations/{id}` | soft delete |
| `PATCH` | `/obligations/{id}/status` | cambiar estado (requiere `version`) |
| `POST` | `/obligations/{id}/documents` | adjuntar documento (mock) |

Modelo de error consistente: `{"error": {"code": "...", "message": "..."}}`. Códigos: `not_found` (404), `conflict` (409), `invalid_transition` / `document_required` / `invalid_company_tax_id` / `validation_error` (422). Docs OpenAPI en `/docs`.

## Levantar el proyecto

### Backend

```bash
cd backend

# macOS + Homebrew Python: apuntar a la libexpat de Homebrew si pyexpat falla
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib:${DYLD_LIBRARY_PATH:-}"

python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"

# Postgres vía docker-compose (recomendado)
docker compose up -d
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/compliance"

# Servidor (las tablas se crean solas al arrancar con create_all)
.venv/bin/uvicorn src.main:app --reload   # http://localhost:8000  ·  docs en /docs
```

`DATABASE_URL` se lee del entorno (default: Postgres local).

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local          # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev                                # http://localhost:3000 → redirige a /es
```

## Tests

```bash
# Backend (unit de dominio + integración HTTP sobre SQLite in-memory)
cd backend
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib:${DYLD_LIBRARY_PATH:-}"
.venv/bin/pytest                           # 23 passed

# Frontend (Vitest + Testing Library)
cd frontend
npm test                                   # flujo del formulario
```

Los tests de backend no necesitan Postgres levantado (usan SQLite in-memory con `StaticPool`).

## Decisiones

- `decisiones-tecnicas.md`: resumen de alto nivel (qué prioricé, qué dejé afuera).
- `registro-decisiones.md`: log de auditoría con cada decisión puntual tomada durante el desarrollo.
