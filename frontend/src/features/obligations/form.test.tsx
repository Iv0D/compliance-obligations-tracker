import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ObligationForm } from "./form";

function fillRequiredFields() {
  fireEvent.change(screen.getByLabelText(/Título/i), {
    target: { value: "Annual report 2026" },
  });
  fireEvent.change(screen.getByLabelText(/Responsable/i), {
    target: { value: "Ana" },
  });
  fireEvent.change(screen.getByLabelText(/Fecha de vencimiento/i), {
    target: { value: "2026-12-01" },
  });
  fireEvent.change(screen.getByLabelText(/Tax ID/i), {
    target: { value: "123456789" },
  });
}

describe("ObligationForm", () => {
  it("submits the collected data", async () => {
    const onSubmit = vi.fn().mockResolvedValue({ ok: true });
    render(<ObligationForm locale="es" onSubmit={onSubmit} />);

    fillRequiredFields();
    fireEvent.click(screen.getByRole("button", { name: /Crear obligación/i }));

    await waitFor(() => expect(onSubmit).toHaveBeenCalledTimes(1));
    expect(onSubmit).toHaveBeenCalledWith(
      expect.objectContaining({
        title: "Annual report 2026",
        owner: "Ana",
        due_date: "2026-12-01",
        company_tax_id: "123456789",
        type: "annual_report",
      })
    );
  });

  it("shows the API error returned by the action", async () => {
    const onSubmit = vi.fn().mockResolvedValue({ error: "invalid_company_tax_id" });
    render(<ObligationForm locale="es" onSubmit={onSubmit} />);

    fillRequiredFields();
    fireEvent.click(screen.getByRole("button", { name: /Crear obligación/i }));

    expect(await screen.findByText("invalid_company_tax_id")).toBeInTheDocument();
  });
});
