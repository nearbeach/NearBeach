// src/plugins/i18n.js
import { createI18n } from "petite-vue-i18n";

// Scrape the page language from the document
const pageLanguage = document.documentElement.lang;

// Setup the internationalization global variable
const i18n = createI18n({
  locale: pageLanguage,
  fallbackLocale: "en",
  legacy: false,
});

export default i18n;
