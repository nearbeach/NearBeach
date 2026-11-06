// composable/safeFetch

/**
 * Drop-in replacement for `fetch` that never rejects.
 *
 * A network failure (offline, DNS, CORS, aborted...) is turned into a synthetic
 * 503 response whose `statusText` is the error message. Callers that already
 * switch on `response.status` and show `response.statusText` in their default
 * branch then handle network failures the same way as server errors.
 */
export async function safeFetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
    try {
        return await fetch(input, init);
    } catch (error) {
        const message = error instanceof Error ? error.message : String(error);

        // statusText must be a valid reason phrase - no line breaks
        return new Response(null, {
            status: 503,
            statusText: message.replace(/[\r\n]+/g, " "),
        });
    }
}
