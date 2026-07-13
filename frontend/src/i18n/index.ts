export const locales = ["es", "en"] as const;
export type Locale = (typeof locales)[number];
export const defaultLocale: Locale = "es";

export type Dictionary = {
  app: { title: string; subtitle: string };
  nav: { dashboard: string };
  locale: { label: string; es: string; en: string };
  status: {
    pending: string;
    in_progress: string;
    submitted: string;
    done: string;
  };
};

const dictionaries: Record<Locale, Dictionary> = {
  es: {
    app: {
      title: "Compliance Obligations Tracker",
      subtitle: "Seguimiento de obligaciones de compliance",
    },
    nav: { dashboard: "Dashboard" },
    locale: { label: "Idioma", es: "Español", en: "English" },
    status: {
      pending: "Pendiente",
      in_progress: "En progreso",
      submitted: "Enviado",
      done: "Completado",
    },
  },
  en: {
    app: {
      title: "Compliance Obligations Tracker",
      subtitle: "Compliance obligations tracking",
    },
    nav: { dashboard: "Dashboard" },
    locale: { label: "Language", es: "Español", en: "English" },
    status: {
      pending: "Pending",
      in_progress: "In progress",
      submitted: "Submitted",
      done: "Done",
    },
  },
};

export function getDictionary(locale: Locale): Dictionary {
  return dictionaries[locale];
}

export function isLocale(value: string): value is Locale {
  return (locales as readonly string[]).includes(value);
}
