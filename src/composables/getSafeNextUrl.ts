// composable/getSafeNextUrl

export function getSafeNextUrl(next: string | null): string {
    // "next" comes from the address bar, so it can be anything - a "javascript:" address, another site, or a trick
    // like "/\t/evil.com" that browsers read as "//evil.com". Only a path on this site is allowed through; everything
    // else lands on the home page.
    if (next === null || !next.startsWith("/")) {
        return "/";
    }

    try {
        const url = new URL(next, window.location.origin);
        return url.origin === window.location.origin
            ? `${url.pathname}${url.search}${url.hash}`
            : "/";
    } catch {
        return "/";
    }
}
