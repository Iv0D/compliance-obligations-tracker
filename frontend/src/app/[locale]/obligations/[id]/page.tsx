import Link from "next/link";
import { notFound, redirect } from "next/navigation";

import { Alert, Button, StatusBadge } from "@/components/ui";
import { getObligation } from "@/features/obligations/api";
import {
  attachDocumentAction,
  changeStatusAction,
  deleteObligationAction,
} from "@/features/obligations/actions";
import { getDictionary, isLocale } from "@/i18n";

type Props = {
  params: Promise<{ locale: string; id: string }>;
  searchParams: Promise<{ error?: string }>;
};

export default async function ObligationDetailPage({ params, searchParams }: Props) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();

  const { error: actionError } = await searchParams;

  let obligation;
  try {
    obligation = await getObligation(id);
  } catch {
    notFound();
  }

  const dictionary = getDictionary(locale);
  const STATUS_LABELS = dictionary.status;
  const isEs = locale === "es";
  const selfUrl = `/${locale}/obligations/${id}`;

  return (
    <div className="space-y-8">
      {/* Back */}
      <Link href={`/${locale}`} className="text-sm text-slate-500 hover:underline">
        ← {isEs ? "Volver al dashboard" : "Back to dashboard"}
      </Link>

      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-xl font-semibold">{obligation.title}</h2>
          <p className="mt-1 text-sm text-slate-500">
            {obligation.type.replace(/_/g, " ")} · {isEs ? "Responsable" : "Owner"}: {obligation.owner}
          </p>
        </div>
        <StatusBadge status={obligation.status} label={STATUS_LABELS[obligation.status]} />
      </div>

      {actionError && <Alert variant="error">{actionError}</Alert>}

      {/* Fields */}
      <section className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm space-y-3">
        <Field label={isEs ? "Vencimiento" : "Due date"} value={obligation.due_date} />
        <Field label={isEs ? "Tax ID" : "Tax ID"} value={obligation.company_tax_id_masked} />
        <Field
          label={isEs ? "¿Requiere documento?" : "Requires document?"}
          value={obligation.requires_document ? (isEs ? "Sí" : "Yes") : "No"}
        />
        {obligation.description && (
          <Field label={isEs ? "Descripción" : "Description"} value={obligation.description} />
        )}
        {obligation.is_overdue && (
          <Alert variant="error">
            {isEs ? "Esta obligación está vencida." : "This obligation is overdue."}
          </Alert>
        )}
      </section>

      {/* Document attachment */}
      {obligation.requires_document && !obligation.has_document && (
        <section className="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <p className="text-sm text-amber-800 mb-3">
            {isEs
              ? "Se requiere un documento antes de enviar."
              : "A document is required before submitting."}
          </p>
          <form
            action={async () => {
              "use server";
              const result = await attachDocumentAction(locale, id);
              redirect(
                "error" in result
                  ? `${selfUrl}?error=${encodeURIComponent(result.error)}`
                  : selfUrl
              );
            }}
          >
            <Button type="submit" variant="secondary">
              {isEs ? "Adjuntar documento (mock)" : "Attach document (mock)"}
            </Button>
          </form>
        </section>
      )}
      {obligation.has_document && (
        <p className="text-sm text-green-700">
          ✓ {isEs ? "Documento adjunto" : "Document attached"}
        </p>
      )}

      {/* Valid transitions */}
      {obligation.valid_transitions.length > 0 && (
        <section>
          <h3 className="mb-3 text-sm font-medium text-slate-700">
            {isEs ? "Cambiar estado" : "Change status"}
          </h3>
          <div className="flex flex-wrap gap-2">
            {obligation.valid_transitions.map((target) => {
              const blocked = target === "submitted" && !obligation.can_submit;
              return (
                <form
                  key={target}
                  action={async () => {
                    "use server";
                    const result = await changeStatusAction(
                      locale, id, target, obligation.version
                    );
                    redirect(
                      "error" in result
                        ? `${selfUrl}?error=${encodeURIComponent(result.error)}`
                        : selfUrl
                    );
                  }}
                >
                  <Button
                    type="submit"
                    variant="secondary"
                    disabled={blocked}
                    title={
                      blocked
                        ? isEs
                          ? "Falta documento"
                          : "Document required"
                        : undefined
                    }
                  >
                    → {STATUS_LABELS[target]}
                  </Button>
                </form>
              );
            })}
          </div>
        </section>
      )}

      {/* Audit trail */}
      {obligation.audit_events.length > 0 && (
        <section>
          <h3 className="mb-3 text-sm font-medium text-slate-700">
            {isEs ? "Historial" : "History"}
          </h3>
          <ol className="space-y-2">
            {obligation.audit_events.map((event, i) => (
              <li key={i} className="text-sm text-slate-600">
                <span className="font-medium">{STATUS_LABELS[event.from_status]}</span>
                {" → "}
                <span className="font-medium">{STATUS_LABELS[event.to_status]}</span>
                <span className="ml-2 text-slate-400 text-xs">
                  {new Date(event.changed_at).toLocaleString(locale)}
                </span>
              </li>
            ))}
          </ol>
        </section>
      )}

      {/* Actions */}
      <div className="flex gap-3 border-t border-slate-200 pt-6">
        <Link
          href={`/${locale}/obligations/${id}/edit`}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          {isEs ? "Editar" : "Edit"}
        </Link>
        <form
          action={async () => {
            "use server";
            await deleteObligationAction(locale, id);
          }}
        >
          <Button type="submit" variant="danger">
            {isEs ? "Eliminar" : "Delete"}
          </Button>
        </form>
      </div>
    </div>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex gap-2 text-sm">
      <span className="w-40 shrink-0 text-slate-500">{label}</span>
      <span className="text-slate-900">{value}</span>
    </div>
  );
}
