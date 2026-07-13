import { notFound } from "next/navigation";

import { ObligationForm } from "@/features/obligations/form";
import { getObligation } from "@/features/obligations/api";
import { updateObligationAction } from "@/features/obligations/actions";
import { isLocale } from "@/i18n";

type Props = { params: Promise<{ locale: string; id: string }> };

export default async function EditObligationPage({ params }: Props) {
  const { locale, id } = await params;
  if (!isLocale(locale)) notFound();
  const isEs = locale === "es";

  let obligation;
  try {
    obligation = await getObligation(id);
  } catch {
    notFound();
  }

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">
        {isEs ? "Editar obligación" : "Edit obligation"}
      </h2>
      <ObligationForm
        locale={locale}
        obligation={obligation}
        onSubmit={async (data) => {
          "use server";
          return updateObligationAction(locale, id, {
            ...data,
            description: data.description || undefined,
            version: obligation.version,
          });
        }}
      />
    </div>
  );
}
