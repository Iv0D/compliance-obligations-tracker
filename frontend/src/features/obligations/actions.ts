"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { ApiResponseError } from "@/lib/http-client";
import type { CreateObligationInput, ObligationStatus, UpdateObligationInput } from "@/lib/types";
import * as api from "./api";

export type ActionResult = { error: string } | { ok: true };

export async function createObligationAction(
  locale: string,
  data: CreateObligationInput
): Promise<ActionResult> {
  try {
    const obligation = await api.createObligation(data);
    revalidatePath(`/${locale}`);
    redirect(`/${locale}/obligations/${obligation.id}`);
  } catch (err) {
    if (err instanceof ApiResponseError) return { error: err.message };
    throw err;
  }
}

export async function updateObligationAction(
  locale: string,
  id: string,
  data: UpdateObligationInput
): Promise<ActionResult> {
  try {
    await api.updateObligation(id, data);
    revalidatePath(`/${locale}/obligations/${id}`);
    return { ok: true };
  } catch (err) {
    if (err instanceof ApiResponseError) return { error: err.message };
    throw err;
  }
}

export async function changeStatusAction(
  locale: string,
  id: string,
  status: ObligationStatus,
  version: number
): Promise<ActionResult> {
  try {
    await api.changeStatus(id, status, version);
    revalidatePath(`/${locale}/obligations/${id}`);
    revalidatePath(`/${locale}`);
    return { ok: true };
  } catch (err) {
    if (err instanceof ApiResponseError) return { error: err.message };
    throw err;
  }
}

export async function attachDocumentAction(
  locale: string,
  id: string
): Promise<ActionResult> {
  try {
    await api.attachDocument(id, "document.pdf", `https://mock-storage/${id}/document.pdf`);
    revalidatePath(`/${locale}/obligations/${id}`);
    return { ok: true };
  } catch (err) {
    if (err instanceof ApiResponseError) return { error: err.message };
    throw err;
  }
}

export async function deleteObligationAction(locale: string, id: string): Promise<void> {
  await api.deleteObligation(id);
  revalidatePath(`/${locale}`);
  redirect(`/${locale}`);
}
