"use client";

import { useState } from "react";

import { Alert, Button } from "@/components/ui";
import type { ObligationDetail, ObligationType } from "@/lib/types";

const TYPES: ObligationType[] = [
  "annual_report",
  "franchise_tax",
  "boi_report",
  "registered_agent_renewal",
];

type FormState = {
  type: ObligationType;
  title: string;
  owner: string;
  due_date: string;
  company_tax_id: string;
  description: string;
  requires_document: boolean;
};

function buildInitial(obligation?: ObligationDetail): FormState {
  return {
    type: obligation?.type ?? "annual_report",
    title: obligation?.title ?? "",
    owner: obligation?.owner ?? "",
    due_date: obligation?.due_date ?? "",
    company_tax_id: "",
    description: obligation?.description ?? "",
    requires_document: obligation?.requires_document ?? false,
  };
}

type Props = {
  obligation?: ObligationDetail;
  locale: string;
  onSubmit: (data: FormState) => Promise<{ error: string } | { ok: true }>;
};

export function ObligationForm({ obligation, locale, onSubmit }: Props) {
  const isEs = locale === "es";
  const [form, setForm] = useState<FormState>(buildInitial(obligation));
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  function set(field: keyof FormState, value: string | boolean) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setPending(true);
    try {
      const result = await onSubmit(form);
      if ("error" in result) setError(result.error);
    } finally {
      setPending(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5 rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      {error && <Alert variant="error">{error}</Alert>}

      <LabeledField label={isEs ? "Tipo" : "Type"}>
        <select
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.type}
          onChange={(e) => set("type", e.target.value as ObligationType)}
          required
        >
          {TYPES.map((t) => (
            <option key={t} value={t}>
              {t.replace(/_/g, " ")}
            </option>
          ))}
        </select>
      </LabeledField>

      <LabeledField label={isEs ? "Título" : "Title"}>
        <input
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.title}
          onChange={(e) => set("title", e.target.value)}
          maxLength={255}
          required
        />
      </LabeledField>

      <LabeledField label={isEs ? "Responsable" : "Owner"}>
        <input
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.owner}
          onChange={(e) => set("owner", e.target.value)}
          maxLength={255}
          required
        />
      </LabeledField>

      <LabeledField label={isEs ? "Fecha de vencimiento" : "Due date"}>
        <input
          type="date"
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.due_date}
          onChange={(e) => set("due_date", e.target.value)}
          required
        />
      </LabeledField>

      <LabeledField label={isEs ? "Tax ID de la empresa" : "Company Tax ID"}>
        <input
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.company_tax_id}
          onChange={(e) => set("company_tax_id", e.target.value)}
          maxLength={50}
          required
        />
        {obligation && (
          <p className="mt-1 text-xs text-slate-500">
            {isEs
              ? `Actual (enmascarado): ${obligation.company_tax_id_masked}. Reingresá el Tax ID completo para guardar.`
              : `Current (masked): ${obligation.company_tax_id_masked}. Re-enter the full Tax ID to save.`}
          </p>
        )}
      </LabeledField>

      <LabeledField label={isEs ? "Descripción (opcional)" : "Description (optional)"}>
        <textarea
          className="w-full rounded border border-slate-300 px-3 py-2 text-sm"
          value={form.description}
          onChange={(e) => set("description", e.target.value)}
          maxLength={2000}
          rows={3}
        />
      </LabeledField>

      <label className="flex items-center gap-2 text-sm">
        <input
          type="checkbox"
          checked={form.requires_document}
          onChange={(e) => set("requires_document", e.target.checked)}
        />
        {isEs ? "Requiere documento" : "Requires document"}
      </label>

      <Button type="submit" disabled={pending}>
        {pending
          ? isEs ? "Guardando..." : "Saving..."
          : obligation
            ? isEs ? "Guardar cambios" : "Save changes"
            : isEs ? "Crear obligación" : "Create obligation"}
      </Button>
    </form>
  );
}

function LabeledField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="block space-y-1">
      <span className="block text-sm font-medium text-slate-700">{label}</span>
      {children}
    </label>
  );
}
