import type { Metadata } from "next";
import { notFound } from "next/navigation";

import "../globals.css";
import { getDictionary, isLocale } from "@/i18n";
import { I18nProvider, LocaleSwitcher } from "@/i18n/provider";

type LayoutProps = {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
};

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string }>;
}): Promise<Metadata> {
  const { locale } = await params;
  if (!isLocale(locale)) {
    return { title: "Compliance Obligations Tracker" };
  }
  const dictionary = getDictionary(locale);
  return { title: dictionary.app.title };
}

export default async function LocaleLayout({ children, params }: LayoutProps) {
  const { locale } = await params;
  if (!isLocale(locale)) {
    notFound();
  }

  const dictionary = getDictionary(locale);

  return (
    <html lang={locale}>
      <body>
        <I18nProvider locale={locale} dictionary={dictionary}>
          <div className="mx-auto min-h-screen max-w-5xl px-4 py-8">
            <header className="mb-8 flex items-start justify-between gap-4 border-b border-slate-200 pb-6">
              <div>
                <h1 className="text-2xl font-semibold">{dictionary.app.title}</h1>
                <p className="mt-1 text-sm text-slate-600">
                  {dictionary.app.subtitle}
                </p>
              </div>
              <LocaleSwitcher />
            </header>
            <main>{children}</main>
          </div>
        </I18nProvider>
      </body>
    </html>
  );
}
