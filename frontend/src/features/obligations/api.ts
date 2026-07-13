import { apiFetch } from "@/lib/http-client";
import type {
  CreateObligationInput,
  DashboardData,
  ObligationDetail,
  ObligationStatus,
  ObligationSummary,
  UpdateObligationInput,
} from "@/lib/types";

export async function getDashboard(): Promise<DashboardData> {
  return apiFetch("/dashboard");
}

export async function listObligations(status?: ObligationStatus): Promise<ObligationSummary[]> {
  const qs = status ? `?status=${status}` : "";
  return apiFetch(`/obligations${qs}`);
}

export async function getObligation(id: string): Promise<ObligationDetail> {
  return apiFetch(`/obligations/${id}`);
}

export async function createObligation(data: CreateObligationInput): Promise<ObligationDetail> {
  return apiFetch("/obligations", { method: "POST", body: JSON.stringify(data) });
}

export async function updateObligation(
  id: string,
  data: UpdateObligationInput
): Promise<ObligationDetail> {
  return apiFetch(`/obligations/${id}`, { method: "PUT", body: JSON.stringify(data) });
}

export async function changeStatus(
  id: string,
  status: ObligationStatus,
  version: number
): Promise<ObligationDetail> {
  return apiFetch(`/obligations/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status, version }),
  });
}

export async function attachDocument(
  id: string,
  filename: string,
  mock_url: string
): Promise<void> {
  return apiFetch(`/obligations/${id}/documents`, {
    method: "POST",
    body: JSON.stringify({ filename, mock_url }),
  });
}

export async function deleteObligation(id: string): Promise<void> {
  return apiFetch(`/obligations/${id}`, { method: "DELETE" });
}
