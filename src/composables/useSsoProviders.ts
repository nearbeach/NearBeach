// composable/useSsoProviders
import {ref} from "vue";

export interface SsoProvider {
    name: string;
    slug: string;
    login_url: string;
}

export function useSsoProviders() {
    const providers = ref<SsoProvider[]>([]);

    async function loadProviders(): Promise<void> {
        // Single sign-on is optional - if we can't find out what is configured, we just offer the password login
        try {
            const response = await fetch("/api/v1/authentication/oidc/providers/");
            if (response.status !== 200) {
                return;
            }

            const data: unknown = await response.json();
            providers.value = Array.isArray(data) ? data : [];
        } catch {
            providers.value = [];
        }
    }

    return {providers, loadProviders};
}
