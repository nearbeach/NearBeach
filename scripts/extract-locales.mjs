#!/usr/bin/env node
/**
 * One-off migration: lift the inline `useI18n({messages: {...}})` blocks out of
 * Vue components into src/locales/<lang>.json.
 *
 *   node scripts/extract-locales.mjs [--dry-run] [file.vue ...]
 *
 * With no files it processes every .vue file under src/ that calls useI18n.
 *
 * For each component it:
 *   - namespaces the keys by the component name (ObjectPriority -> object_priority)
 *   - merges them into src/locales/<lang>.json
 *   - rewrites useI18n({...}) to useI18n() and t("key") to t("namespace.key")
 *
 * Anything it can't convert safely (dynamic keys, other useI18n options,
 * missing keys) is reported and that component is left untouched.
 */
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import {fileURLToPath} from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const srcDir = path.join(root, "src");
const localeDir = path.join(srcDir, "locales");

const args = process.argv.slice(2);
const dryRun = args.includes("--dry-run");
const fileArgs = args.filter((a) => !a.startsWith("--"));

function walk(dir) {
    return fs.readdirSync(dir, {withFileTypes: true}).flatMap((entry) => {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) return walk(full);
        return entry.name.endsWith(".vue") ? [full] : [];
    });
}

/** Index of the bracket that closes the one at `start`, skipping strings. */
function matchBracket(text, start) {
    const open = text[start];
    const close = {"{": "}", "(": ")"}[open];
    let depth = 0;
    for (let i = start; i < text.length; i++) {
        const ch = text[i];
        if (ch === '"' || ch === "'" || ch === "`") {
            for (i++; i < text.length && text[i] !== ch; i++) {
                if (text[i] === "\\") i++;
            }
        } else if (ch === open) {
            depth++;
        } else if (ch === close && --depth === 0) {
            return i;
        }
    }
    throw new Error("unbalanced brackets");
}

const namespaceOf = (file) =>
    path.basename(file, ".vue").replace(/([a-z0-9])([A-Z])/g, "$1_$2").toLowerCase();

/** {a: {b: "x"}} -> {"a.b": "x"}. petite-vue-i18n only looks keys up flat. */
const flattenEntries = (obj, prefix = "") =>
    Object.entries(obj).flatMap(([k, v]) =>
        typeof v === "object" && v !== null ? flattenEntries(v, `${prefix}${k}.`) : [[`${prefix}${k}`, v]],
    );

const flatten = (obj) => flattenEntries(obj).map(([k]) => k);

function convert(file, source) {
    const callStart = source.indexOf("useI18n(");
    if (callStart === -1) return {skip: "no useI18n call"};

    const parenOpen = callStart + "useI18n".length;
    const parenClose = matchBracket(source, parenOpen);
    const argText = source.slice(parenOpen + 1, parenClose).trim();

    if (argText === "") return {skip: "already uses the global instance"};

    let options;
    try {
        options = vm.runInNewContext(`(${argText})`);
    } catch (e) {
        return {skip: `could not evaluate useI18n options: ${e.message}`};
    }

    const extra = Object.keys(options).filter((k) => k !== "messages");
    if (extra.length > 0) return {skip: `useI18n has other options: ${extra.join(", ")}`};
    if (!options.messages?.en) return {skip: "no English messages"};

    const ns = namespaceOf(file);
    const enKeys = new Set(flatten(options.messages.en));

    // Rewrite the call, then the t() usages (script + template)
    const head = source.slice(0, parenOpen + 1);
    const tail = source.slice(parenClose);
    let body = head + tail;

    const problems = [];
    const used = new Set();
    body = body.replace(/(?<![\w.$])(\$?t)\(\s*(['"])([\w.]+)\2/g, (_m, fn, quote, key) => {
        used.add(key);
        if (!enKeys.has(key)) problems.push(`t("${key}") is not defined in the English messages`);
        return `${fn}(${quote}${ns}.${key}${quote}`;
    });

    // Template-literal keys (t(`title_${x}`)) can't be checked, but the namespace can still be added
    body = body.replace(/(?<![\w.$])(\$?t)\(\s*`(?!\w+\.)/g, (_m, fn) => `${fn}(\`${ns}.`);

    // Anything else calling t/te/tm/rt is dynamic and needs a human
    const dynamic = [...body.matchAll(/(?<![\w.$])\$?(?:t|te|tm|rt)\(\s*(?!['"][\w.]+['"])([^)]{0,40})/g)]
        .filter((m) => !m[0].includes(`${ns}.`))
        .map((m) => m[0]);
    const manual = dynamic.map((d) => `MANUAL: non-literal key needs a hand edit: ${d}`);

    const unused = [...enKeys].filter((k) => !used.has(k));
    const warnings = [...manual, ...(unused.length ? [`unused keys: ${unused.join(", ")}`] : [])];

    return {ns, messages: options.messages, body, problems, warnings};
}

const files = fileArgs.length
    ? fileArgs.map((f) => path.resolve(f))
    : walk(srcDir).filter((f) => fs.readFileSync(f, "utf8").includes("useI18n"));

const locales = {};
const writes = [];
let converted = 0;

for (const file of files) {
    const rel = path.relative(root, file);
    const result = convert(file, fs.readFileSync(file, "utf8"));

    if (result.skip) {
        console.log(`SKIP  ${rel}: ${result.skip}`);
        continue;
    }
    if (result.problems.length) {
        console.log(`FAIL  ${rel}`);
        result.problems.forEach((p) => console.log(`        - ${p}`));
        continue;
    }

    for (const [lang, messages] of Object.entries(result.messages)) {
        const localeFile = path.join(localeDir, `${lang}.json`);
        locales[lang] ??= fs.existsSync(localeFile) ? JSON.parse(fs.readFileSync(localeFile, "utf8")) : {};
        const entries = flattenEntries(messages).map(([k, v]) => [`${result.ns}.${k}`, v]);
        const clash = entries.find(([k, v]) => k in locales[lang] && locales[lang][k] !== v);
        if (clash) {
            console.log(`FAIL  ${rel}: "${clash[0]}" already exists in ${lang}.json with different content`);
            continue;
        }
        Object.assign(locales[lang], Object.fromEntries(entries));
    }

    writes.push([file, result.body]);
    converted++;
    console.log(`OK    ${rel} -> ${result.ns} (${Object.keys(result.messages).join(", ")})`);
    result.warnings.forEach((w) => console.log(`        ! ${w}`));
}

// Every language should have the same keys as English
for (const [lang, data] of Object.entries(locales)) {
    if (lang === "en") continue;
    const missing = Object.keys(locales.en ?? {}).filter((k) => !(k in data));
    if (missing.length) console.log(`WARN  ${lang}.json is missing: ${missing.join(", ")}`);
}

if (dryRun) {
    console.log(`\nDry run: ${converted} component(s) would be converted. Nothing written.`);
} else {
    fs.mkdirSync(localeDir, {recursive: true});
    for (const [lang, data] of Object.entries(locales)) {
        const sorted = Object.fromEntries(Object.entries(data).sort(([a], [b]) => a.localeCompare(b)));
        fs.writeFileSync(path.join(localeDir, `${lang}.json`), JSON.stringify(sorted, null, 2) + "\n");
    }
    writes.forEach(([file, body]) => fs.writeFileSync(file, body));
    console.log(`\nConverted ${converted} component(s).`);
}
