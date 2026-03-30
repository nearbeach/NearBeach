// composables/failedValidation.ts

export function failedValidation(fieldValidation: Record<string, boolean>) : boolean {
    // If field validation is undefined - fail by default
    if (fieldValidation === undefined) {
        return true;
    }

    // Any false exist -> we fail
    return Object.keys(fieldValidation).some(row => !fieldValidation[row]);
}