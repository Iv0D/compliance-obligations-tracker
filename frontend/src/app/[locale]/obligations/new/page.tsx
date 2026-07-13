import { notFound } from "next/navigation";

import { ObligationForm } from "@/features/obligations/form";
import { createObligationAction } from "@/features/obligations/actions";
import { isLocale } from "@/i18n";

type Props = { params: Promise<{ locale: string }> };

export default async function NewObligationPage({ params }: Props) {
  const { locale } = await params;
  if (!isLocale(locale)) notFound();
  const isEs = locale === "es";

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">
        {isEs ? "Nueva obligación" : "New obligation"}
      </h2>
      <ObligationForm
        locale={locale}
        onSubmit={async (data) => {
          "use server";
          return createObligationAction(locale, {
            ...data,
            description: data.description || undefined,
          });
        }}
      />
    </div>
  );
}
