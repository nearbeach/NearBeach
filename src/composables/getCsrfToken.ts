// composable/getCsrfToken

export function getCsrfToken(): string {
    // The cookie has to start the string or follow a "; " - otherwise "other_csrftoken=..." would match too
    const CSRF_TOKEN : RegExpMatchArray | null = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return CSRF_TOKEN === null
        ? ""
        : CSRF_TOKEN[1];
}
