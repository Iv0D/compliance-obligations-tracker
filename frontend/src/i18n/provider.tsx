"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { createContext, useContext } from "react";

import { type Dictionary, type Locale, locales } from "@/i18n";

type I18nContextValue = {
  locale: Locale;
  dictionary: Dictionary;
};

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({
  locale,
  dictionary,
  children,
}: I18nContextValue & { children: React.ReactNode }) {
  return (
    <I18nContext.Provider value={{ locale, dictionary }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useI18n(): I18nContextValue {
  const value = useContext(I18nContext);
  if (!value) {
    throw new Error("useI18n must be used within I18nProvider");
  }
  return value;
}

export function LocaleSwitcher() {
  const { locale, dictionary } = useI18n();
  const pathname = usePathname();

  return (
    <nav aria-label={dictionary.locale.label} className="flex gap-2 text-sm">
      {locales.map((target) => {
        const href = pathname.replace(`/${locale}`, `/${target}`);
        const isActive = target === locale;
        return (
          <Link
            key={target}
            href={href}
            className={
              isActive
                ? "font-medium text-slate-900"
                : "text-slate-500 hover:text-slate-900"
            }
          >
            {dictionary.locale[target]}
          </Link>
        );
      })}
    </nav>
  );
}
