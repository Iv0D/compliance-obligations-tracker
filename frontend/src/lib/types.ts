export type ObligationType =
  | "annual_report"
  | "franchise_tax"
  | "boi_report"
  | "registered_agent_renewal";

export type ObligationStatus =
  | "pending"
  | "in_progress"
  | "submitted"
  | "done";

export type AuditEvent = {
  from_status: ObligationStatus;
  to_status: ObligationStatus;
  changed_at: string;
};

export type ObligationSummary = {
  id: string;
  type: ObligationType;
  title: string;
  owner: string;
  due_date: string;
  status: ObligationStatus;
  description: string | null;
  requires_document: boolean;
  company_tax_id_masked: string;
  is_overdue: boolean;
  version: number;
  created_at: string | null;
  updated_at: string | null;
};

export type ObligationDetail = ObligationSummary & {
  audit_events: AuditEvent[];
  valid_transitions: ObligationStatus[];
  can_submit: boolean;
  has_document: boolean;
};

export type DashboardData = {
  total: number;
  by_status: Record<ObligationStatus, number>;
  overdue: number;
  upcoming: number;
};

export type ApiError = {
  code: string;
  message: string;
};

export type CreateObligationInput = {
  type: ObligationType;
  title: string;
  owner: string;
  due_date: string;
  company_tax_id: string;
  description?: string;
  requires_document?: boolean;
};

export type UpdateObligationInput = CreateObligationInput & {
  version: number;
};
