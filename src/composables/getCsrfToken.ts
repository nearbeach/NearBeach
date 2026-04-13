// composable/getCsrfToken

export function getCsrfToken(): string {
    const CSRF_TOKEN : RegExpMatchArray | null = document.cookie.match(new RegExp(`csrftoken=([^;]+)`));
    return CSRF_TOKEN === null
        ? ""
        : CSRF_TOKEN[0].replace("csrftoken=", "");
}