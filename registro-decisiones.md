# Registro de decisiones del usuario

Archivo vivo. El asistente actualiza este registro automáticamente cada vez que el usuario toma una decisión, se sale del plan, o corrige al asistente.

**No confundir con** `decisiones-tecnicas.md` (entregable final de la prueba). Este archivo es el historial crudo de elecciones durante el desarrollo.

---

## Cómo leer cada entrada

| Campo | Significado |
|-------|-------------|
| **Tipo** | `decisión` · `desvío del plan` · `corrección al asistente` |
| **Contexto** | Situación en la que surgió la decisión |
| **Decisión** | Qué eligió el usuario |
| **Motivo** | Por qué (si lo expresó) |
| **Impacto** | Qué tareas, archivos o enfoque cambia |

---

## Decisiones

### 001 — Arquitectura simple (4 capas)

- **Fecha:** 2026-07-08
- **Tipo:** decisión
- **Contexto:** Al proponer la estructura del proyecto, el usuario pidió confirmar si la arquitectura era simple.
- **Decisión:** Mantener Clean Architecture liviana: `domain` → `application` → `infrastructure` + `interfaces/http`. Sin controllers separados, sin unit-of-work, sin hooks en frontend.
- **Motivo:** Alineado con `decisiones-tecnicas.md`: scope chico, fácil de explicar y defender.
- **Impacto:** Estructura de carpetas del repo; commits `chore` separados de `feat`.

---

### 002 — Solo estructura, sin código

- **Fecha:** 2026-07-08
- **Tipo:** decisión
- **Contexto:** Tras definir la estructura, el usuario pidió implementarla como MVP mínimo.
- **Decisión:** Crear únicamente carpetas y archivos vacíos. No escribir lógica de negocio ni configuración funcional todavía.
- **Motivo:** Separar boilerplate de contribuciones; avanzar paso a paso.
- **Impacto:** Todos los `.py` y `.tsx` quedaron vacíos; solo `README.md` y `.gitignore` con contenido.

---

### 003 — Dividir en tareas pequeñas antes de codear

- **Fecha:** 2026-07-08
- **Tipo:** decisión
- **Contexto:** El usuario compartió el PDF de la prueba técnica y pidió un plan incremental.
- **Decisión:** 22 tareas en 8 fases, cada una mapeable a un commit limpio (`chore` / `feat` / `test` / `docs`). No empezar a codear hasta que el plan esté acordado.
- **Motivo:** Contar una historia de desarrollo defendible; respetar regla de commits del proyecto.
- **Impacto:** Orden de implementación definido; lista de tareas en sesión.

---

### 004 — PostgreSQL + docker-compose

- **Fecha:** 2026-07-08
- **Tipo:** decisión
- **Contexto:** Elección de motor de persistencia antes de implementar (tareas 2 y 9 del plan).
- **Decisión:** PostgreSQL con docker-compose (no SQLite).
- **Motivo:** Es lo recomendado en la consigna; hace más creíble defender concurrencia / optimistic locking.
- **Impacto:** Tarea 2 (boilerplate persistencia) y tarea 9 (repositorio + optimistic lock) usan Postgres.

---

### 005 — Arrancar por el dominio, no por fundaciones

- **Fecha:** 2026-07-08
- **Tipo:** desvío del plan
- **Contexto:** El plan original sugería Fase 0 (fundaciones) → Fase 1 (boilerplate backend) → Fase 2 (dominio). Se preguntó por dónde empezar.
- **Decisión:** Saltar directo a Fase 2 — Dominio (tareas 3–7). Volver al boilerplate (tareas 0–2) justo antes de conectar HTTP.
- **Motivo:** El dominio es lo que más pesa en la rúbrica (25% arquitectura + 15% integridad + 10% overdue).
- **Impacto:** Dominio se implementa en Python puro, testeable sin FastAPI ni DB levantada. Tareas 0–2 se posponen pero no se descartan.

---

### 006 — Registro automático de decisiones

- **Fecha:** 2026-07-08
- **Tipo:** decisión
- **Contexto:** Antes de empezar a codear el dominio, el usuario pidió un archivo dedicado.
- **Decisión:** Crear `registro-decisiones.md` y mantenerlo actualizado automáticamente con cada decisión futura del usuario.
- **Motivo:** Trazabilidad de elecciones propias; distinguir decisiones originales vs. correcciones al asistente.
- **Impacto:** Este archivo. El asistente agrega entradas numeradas sin pedir confirmación extra.

---

### 007 — Adaptar el proyecto a los diagramas (Excalidraw)

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** El usuario compartió 3 diagramas (arquitectura, máquina de estados, ER) y pidió adaptar la estructura a ellos, paso a paso, revisando cada stage
- **Decisión:** Alinear la estructura con los diagramas: Clean Layered Architecture + DDD-lite, patrones Repository + Service Layer + State Machine + DTOs + Optimistic Locking + Audit Trail. Modelo de datos de 3 tablas (`obligations`, `documents`, `audit_events`).
- **Motivo:** Coherencia entre lo diseñado y lo entregado; es lo que más pesa en la rúbrica de arquitectura y se defiende mejor.
- **Impacto:** README actualizado con modelo de 3 tablas y flujo de capas. Base para la decisión 008.

---

### 008 — Documentos como entidad/tabla separada (Opción A)

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** Los diagramas modelan `documents` como tabla separada, pero el scaffold inicial asumía un campo `document_ref` string en `Obligation`. Se evaluaron trade-offs (Opción A: tabla separada vs. Opción B: campo string).
- **Decisión:** Opción A — `documents` como entidad/tabla separada (`id`, `obligation_id`, `filename`, `mock_url`, `created_at`), con implementación deliberadamente mínima. Subida de archivo **mock** (no real, porque la subida real es stretch). El invariante doc-gated consulta al repositorio "¿existe al menos un documento?".
- **Motivo:** Fidelidad a los diagramas que se van a defender; modela mejor el dominio real (multi-documento con metadata); evita inconsistencia diagrama↔código en la defensa.
- **Impacto:** Se agregaron `domain/entities/document.py`, `application/ports/document_repository.py`, `application/use_cases/attach_document.py`, `infrastructure/database/models/document_model.py` y `frontend/.../components/document-attachment.tsx`. Endpoint de adjuntar como sub-recurso `POST /obligations/{id}/documents`. Se descartó el campo `document_ref` string.

---

### 009 — Overdue: due_date = hoy no está vencida

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** Caso borde pendiente antes de implementar el dominio. ¿Una obligación con `due_date` igual a hoy cuenta como vencida?
- **Decisión:** `due_date = hoy` → **no** está vencida. Regla: `is_overdue = due_date < today AND status NOT IN (submitted, done)`.
- **Motivo:** "Vence hoy" implica que todavía está a tiempo; solo pasa a overdue cuando la fecha ya pasó.
- **Impacto:** `domain/services/overdue.py`, tests de dominio, KPIs del dashboard y resalte en listado.

---

### 010 — KPI "próximas a vencer": ventana de 7 días

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** El dashboard pide KPI de obligaciones próximas a vencer, pero no define la ventana.
- **Decisión:** Próximas a vencer = `due_date` entre hoy y hoy + 7 días (inclusive), excluyendo las ya vencidas y las en `submitted`/`done`.
- **Motivo:** Ventana corta, simple de explicar y alineada con recordatorios típicos de compliance.
- **Impacto:** `GetDashboardKpis` use case, endpoint dashboard, KPI en frontend.

---

### 011 — Transición al mismo estado: rechazar (422)

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** Caso borde: `change_status` pide el estado que la obligación ya tiene (doble click, request desactualizado).
- **Decisión:** Rechazar con **422**, sin persistir nada ni crear audit event. No se considera `status → status` una transición válida.
- **Motivo:** Coherente con la máquina de estados; el backend expone `valid_transitions` y el front no debería ofrecer esa acción; audit trail limpio.
- **Impacto:** `domain/services/state_machine.py`, `ChangeStatus` use case, modelo de error HTTP, UI de transiciones.

---

### 012 — Reparar Python local con venv + pip

- **Fecha:** 2026-07-09
- **Tipo:** decisión
- **Contexto:** `python3.14` de Homebrew fallaba al importar `pyexpat` (pip/pytest inutilizables). Se pidió reparar el entorno y usar venv + pip.
- **Decisión:** `brew reinstall expat python@3.14` y correr Python/tests con `DYLD_LIBRARY_PATH="/opt/homebrew/opt/expat/lib"`. Venv en `backend/.venv` con pytest.
- **Motivo:** Recuperar un runner de tests reproducible sin introducir otra herramienta (uv/docker) en este paso.
- **Impacto:** `backend/pyproject.toml`, `backend/tests/unit/domain/test_domain_rules.py`, README con comando de tests.

---

### 013 — Sesión por request y versión en el body

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** La capa HTTP necesita definir cómo se abre/commitea la transacción y cómo llega la `version` para optimistic locking en `update` y `change-status`.
- **Decisión:** Una sesión SQLAlchemy por request (dependencia `get_session` con commit al final / rollback ante excepción). La `version` esperada viaja en el body JSON de `PUT /obligations/{id}` y `PATCH /obligations/{id}/status`, no en un header `If-Match`.
- **Motivo:** Diff mínimo y explícito; evita depender de convenciones de headers y mantiene el contrato simple para el frontend.
- **Impacto:** `interfaces/http/dependencies.py`, `interfaces/http/routes/obligations.py`, schemas de request.

---

### 014 — Modelo de error HTTP uniforme

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** La consigna pide un modelo de error consistente (404/409/422). FastAPI/Pydantic devuelven por defecto un formato distinto para errores de validación.
- **Decisión:** Todas las respuestas de error usan `{"error": {"code": "...", "message": "..."}}`. Mapeo: `not_found`→404, `conflict`→409, `invalid_transition`/`document_required`/`invalid_company_tax_id`/`validation_error`→422. Se normaliza también `RequestValidationError`.
- **Motivo:** Contrato único para el frontend, más fácil de consumir y de testear.
- **Impacto:** `interfaces/http/errors/http_errors.py`, schemas de respuesta (`ErrorResponse`).

---

### 015 — Borrado: soft delete

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** Faltaba la "D" del CRUD. Había que decidir borrado físico vs lógico.
- **Decisión:** Soft delete. Se agrega `deleted_at` (nullable) a `Obligation`; `DELETE /obligations/{id}` marca la fila como borrada. Listado y dashboard excluyen borradas; `GET` de una borrada devuelve 404. Se preserva el audit trail.
- **Motivo:** Dominio de compliance: conviene no perder historial ni trazabilidad; el borrado es reversible/auditable.
- **Impacto:** `domain/entities/obligation.py`, modelo ORM, repos (filtro `deleted_at IS NULL`), nuevo use case + ruta `DELETE`.

---

### 016 — i18n con diccionario propio (sin librería)

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** El stack pide i18n es/en "sin librería pesada".
- **Decisión:** Diccionario propio mínimo (provider de React + JSON `es`/`en`), sin dependencia externa.
- **Motivo:** Cumple la restricción del stack y mantiene el bundle liviano; suficiente para el alcance.
- **Impacto:** `frontend` (provider i18n, archivos de traducción, selector de idioma).

---

### 017 — Tests de integración sobre SQLite in-memory

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** Tarea 12 necesita una base para los tests de integración del backend.
- **Decisión:** SQLite in-memory con `StaticPool` (conexión compartida) y `dependency_overrides` de la sesión; sin Docker en CI.
- **Motivo:** Rápido y reproducible. Se documenta que Postgres es la base de prod (docker-compose).
- **Impacto:** `backend/tests/integration/`, fixture de app + sesión de test.

---

### 018 — Adjuntar documento: form mock simple

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** El documento es mock (la consigna lo permite).
- **Decisión:** Botón/form simple que genera un documento mock (`filename` + `mock_url`), sin upload real de archivos.
- **Motivo:** Diff mínimo; lo relevante es la invariante doc-gated, no la mecánica de upload.
- **Impacto:** `frontend` (acción de adjuntar en el detalle), endpoint `POST /obligations/{id}/documents` ya existente.

---

### 019 — Logging seguro mínimo con redacción

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** Tarea 11: la consigna exige que `companyTaxId` nunca se loguee.
- **Decisión:** Logging mínimo con un filtro/función de redacción (`redact_tax_id`) aplicado en logs de cambios de estado. No se serializa el taxId crudo en respuestas ni en logs.
- **Motivo:** Cubre el requisito de dato sensible sin agregar infraestructura de logging compleja.
- **Impacto:** `backend` (config de logging + uso de `redact_tax_id` en la capa de aplicación/HTTP).

---

### 020 — Filtro del dashboard: solo por status

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** El backend ya filtra por `status`; se evaluó sumar `type` y/o toggle "solo vencidas".
- **Decisión:** Mantener solo el filtro por `status` (mínimo).
- **Motivo:** Alcance acotado; menos superficie para probar. Se puede extender luego si sobra tiempo.
- **Impacto:** `frontend` (control de filtro por status), endpoint `GET /obligations?status=` ya existente.

---

### 021 — Tax ID obligatorio al editar

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** El backend sobrescribe `company_tax_id` con lo recibido en `PUT`. El form de edición no puede prellenar el valor crudo (solo se conoce enmascarado), y mandar el enmascarado corrompería el dato.
- **Decisión:** El campo Tax ID es obligatorio también al editar; el usuario reingresa el valor completo. Sin cambios en backend.
- **Motivo:** Diff mínimo y coherente con el dato sensible (nunca se envía el crudo al cliente). Se muestra el enmascarado actual como referencia.
- **Impacto:** `frontend/features/obligations/form.tsx`, `app/[locale]/obligations/[id]/edit/page.tsx`.

---

### 022 — Test de frontend con Vitest + Testing Library

- **Fecha:** 2026-07-12
- **Tipo:** decisión
- **Contexto:** La Tarea 20 pide un test de un flujo de frontend; no había framework instalado.
- **Decisión:** Vitest + Testing Library (jsdom), sin navegador. Se testea el flujo del formulario: envío con datos correctos y render del error devuelto por la Server Action.
- **Motivo:** Rápido y sin dependencias pesadas ni backend levantado; suficiente para demostrar el flujo.
- **Impacto:** `frontend/vitest.config.ts`, `vitest.setup.ts`, `features/obligations/form.test.tsx`, script `test` en `package.json`.

---

### 023 — Soft delete anonimiza el tax id

- **Fecha:** 2026-07-13
- **Tipo:** decisión
- **Contexto:** El soft delete (decisión 015) conserva la fila, pero dejaba vivo el `company_tax_id` (dato sensible) tras "borrar". Trade-off entre auditoría (soft) y privacidad (hard delete).
- **Decisión:** Mantener soft delete pero anonimizar `company_tax_id` (se setea a cadena vacía) en el mismo `UPDATE` que marca `deleted_at`. Se preserva el audit trail y se elimina el dato sensible.
- **Motivo:** Lo mejor de ambos mundos con diff mínimo: trazabilidad intacta + sin dato sensible remanente. Las filas borradas no se reconstruyen a dominio (se excluyen en lecturas), así que la cadena vacía no rompe el value object.
- **Impacto:** `infrastructure/repositories/postgres_obligation_repository.py` (`soft_delete`), test `test_soft_delete_anonymizes_tax_id`.

---

## Correcciones al asistente

_Ninguna registrada todavía._

Cuando el usuario corrija al asistente, la entrada irá aquí con **Tipo: corrección al asistente** y se detallará qué dijo o hizo mal el asistente y qué pidió el usuario en su lugar.

---

## Plantilla para nuevas entradas

```md
### NNN — Título corto

- **Fecha:** YYYY-MM-DD
- **Tipo:** decisión | desvío del plan | corrección al asistente
- **Contexto:** …
- **Decisión:** …
- **Motivo:** … (si aplica)
- **Corrección:** … (solo si el asistente se equivocó y el usuario lo corrigió)
- **Impacto:** …
```
