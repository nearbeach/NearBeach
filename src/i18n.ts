import {createI18n} from "petite-vue-i18n";
import en from "@/locales/en.json";

// English is the fallback so it is bundled up front. Every other language is
// its own chunk and is only downloaded when the page asks for it.
const localeLoaders = import.meta.glob<{default: typeof en}>(
    ["./locales/*.json", "!./locales/en.json"],
);

// Scrape the page language from the document
const pageLanguage = document.documentElement.lang || "en";

// Set up the internationalization global variable
const i18n = createI18n<[typeof en], string>({
    locale: pageLanguage,
    fallbackLocale: "en",
    legacy: false,
    messages: {en},
});

/**
 * Download the messages for a locale and register them. Tries the exact locale
 * (e.g. "ja-JP") and then the base language (e.g. "ja"). An unknown locale is
 * left alone, so the "en" fallback is used.
 *
 * Await this before mounting the app so the first render is already translated.
 */
export async function loadLocale(locale: string = pageLanguage): Promise<void> {
    const candidates = [locale, locale.split("-")[0]];

    for (const candidate of candidates) {
        if (candidate === "en" || i18n.global.availableLocales.includes(candidate)) {
            return;
        }

        const loader = localeLoaders[`./locales/${candidate}.json`];
        if (loader === undefined) {
            continue;
        }

        i18n.global.setLocaleMessage(candidate, (await loader()).default);
        return;
    }
}

export default i18n;
