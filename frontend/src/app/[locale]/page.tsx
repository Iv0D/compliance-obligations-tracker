import Link from "next/link";
import { notFound } from "next/navigation";

import { StatusBadge } from "@/components/ui";
import { getDashboard, listObligations } from "@/features/obligations/api";
import { getDictionary, isLocale } from "@/i18n";
import type { ObligationStatus } from "@/lib/types";

type Props = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ status?: string }>;
};

const STATUS_KEYS: ObligationStatus[] = ["pending", "in_progress", "submitted", "done"];

export default async function DashboardPage({ params, searchParams }: Props) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();

  const dictionary = getDictionary(locale);
  const { status: rawStatus } = await searchParams;
  const statusFilter = STATUS_KEYS.includes(rawStatus as ObligationStatus)
    ? (rawStatus as ObligationStatus)
    : undefined;

  const [kpis, obligations] = await Promise.all([
    getDashboard(),
    listObligations(statusFilter),
  ]);

  return (
    <div className="space-y-8">
      {/* KPIs */}
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <KpiCard label={locale === "es" ? "Total" : "Total"} value={kpis.total} />
        <KpiCard label={locale === "es" ? "Vencidas" : "Overdue"} value={kpis.overdue} accent="red" />
        <KpiCard label={locale === "es" ? "Próximas a vencer" : "Upcoming"} value={kpis.upcoming} accent="amber" />
        {kpis.by_status.done !== undefined && (
          <KpiCard label={locale === "es" ? "Completadas" : "Done"} value={kpis.by_status.done} accent="green" />
        )}
      </div>

      {/* Filter */}
      <div className="flex gap-2 flex-wrap">
        <FilterLink locale={locale} current={statusFilter} value={undefined} label={locale === "es" ? "Todas" : "All"} />
        {STATUS_KEYS.map((s) => (
          <FilterLink key={s} locale={locale} current={statusFilter} value={s} label={dictionary.status[s]} />
        ))}
      </div>

      {/* List */}
      {obligations.length === 0 ? (
        <p className="text-sm text-slate-500">
          {locale === "es" ? "No hay obligaciones." : "No obligations found."}
        </p>
      ) : (
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="border-b border-slate-200 text-left text-xs text-slate-500">
              <th className="pb-2 pr-4">{locale === "es" ? "Título" : "Title"}</th>
              <th className="pb-2 pr-4">{locale === "es" ? "Tipo" : "Type"}</th>
              <th className="pb-2 pr-4">{locale === "es" ? "Estado" : "Status"}</th>
              <th className="pb-2 pr-4">{locale === "es" ? "Vencimiento" : "Due date"}</th>
              <th className="pb-2">{locale === "es" ? "Responsable" : "Owner"}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {obligations.map((o) => (
              <tr
                key={o.id}
                className={`hover:bg-slate-50 ${o.is_overdue ? "bg-red-50" : ""}`}
              >
                <td className="py-2 pr-4">
                  <Link href={`/${locale}/obligations/${o.id}`} className="font-medium hover:underline">
                    {o.title}
                  </Link>
                  {o.is_overdue && (
                    <span className="ml-2 text-xs text-red-600 font-medium">
                      {locale === "es" ? "vencida" : "overdue"}
                    </span>
                  )}
                </td>
                <td className="py-2 pr-4 text-slate-600">{o.type.replace(/_/g, " ")}</td>
                <td className="py-2 pr-4">
                  <StatusBadge status={o.status} label={dictionary.status[o.status]} />
                </td>
                <td className="py-2 pr-4 text-slate-600">{o.due_date}</td>
                <td className="py-2 text-slate-600">{o.owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <Link
        href={`/${locale}/obligations/new`}
        className="inline-block rounded bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-700"
      >
        {locale === "es" ? "+ Nueva obligación" : "+ New obligation"}
      </Link>
    </div>
  );
}

function KpiCard({
  label,
  value,
  accent = "default",
}: {
  label: string;
  value: number;
  accent?: "red" | "amber" | "green" | "default";
}) {
  const accentStyle = {
    red: "text-red-600",
    amber: "text-amber-600",
    green: "text-green-600",
    default: "text-slate-900",
  }[accent];
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs text-slate-500">{label}</p>
      <p className={`mt-1 text-3xl font-bold ${accentStyle}`}>{value}</p>
    </div>
  );
}

function FilterLink({
  locale,
  current,
  value,
  label,
}: {
  locale: string;
  current: ObligationStatus | undefined;
  value: ObligationStatus | undefined;
  label: string;
}) {
  const isActive = current === value;
  const href = value ? `/${locale}?status=${value}` : `/${locale}`;
  return (
    <Link
      href={href}
      className={`rounded-full px-3 py-1 text-xs capitalize ${
        isActive
          ? "bg-slate-900 text-white"
          : "border border-slate-300 text-slate-600 hover:bg-slate-50"
      }`}
    >
      {label}
    </Link>
  );
}
