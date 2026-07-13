import type { ObligationStatus } from "@/lib/types";

export function Button({
  children,
  variant = "primary",
  disabled,
  className = "",
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "danger";
}) {
  const base = "rounded px-3 py-1.5 text-sm font-medium transition disabled:opacity-50";
  const variants = {
    primary: "bg-slate-900 text-white hover:bg-slate-700",
    secondary: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50",
    danger: "bg-red-600 text-white hover:bg-red-500",
  };
  return (
    <button disabled={disabled} className={`${base} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}

const STATUS_STYLES: Record<ObligationStatus, string> = {
  pending: "bg-slate-100 text-slate-700",
  in_progress: "bg-blue-100 text-blue-700",
  submitted: "bg-amber-100 text-amber-700",
  done: "bg-green-100 text-green-700",
};

const STATUS_LABELS: Record<ObligationStatus, string> = {
  pending: "Pendiente",
  in_progress: "En progreso",
  submitted: "Enviado",
  done: "Completado",
};

export function StatusBadge({ status }: { status: ObligationStatus }) {
  return (
    <span
      className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_STYLES[status]}`}
    >
      {STATUS_LABELS[status]}
    </span>
  );
}

export function Alert({ children, variant = "error" }: { children: React.ReactNode; variant?: "error" | "info" }) {
  const styles = {
    error: "border-red-200 bg-red-50 text-red-800",
    info: "border-blue-200 bg-blue-50 text-blue-800",
  };
  return (
    <div className={`rounded border px-4 py-3 text-sm ${styles[variant]}`}>{children}</div>
  );
}

export function Skeleton({ className = "" }: { className?: string }) {
  return <div className={`animate-pulse rounded bg-slate-200 ${className}`} />;
}
