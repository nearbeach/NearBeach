import {describe, expect, test} from "vitest";
import en from "./en.json";

const otherLocales = import.meta.glob<{default: Record<string, string>}>(
    ["./*.json", "!./en.json"],
    {eager: true},
);

describe("locale files", () => {
    const enKeys = Object.keys(en);

    test.each(Object.entries(otherLocales))("%s has exactly the keys English has", (_path, module) => {
        const keys = Object.keys(module.default);

        expect(enKeys.filter((k) => !keys.includes(k))).toEqual([]);
        expect(keys.filter((k) => !enKeys.includes(k))).toEqual([]);
    });
});
