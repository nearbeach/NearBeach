// stores/error.ts
import {defineStore} from 'pinia';

export const useErrorStore = defineStore("error", {
	state: () => {
		return {
			message: "" as string,
		};
	},
	actions: {
		setError(error: any | unknown) {
			if (error instanceof Error) {
				this.message = error.message;
			} else {
				this.message = String(error);
			}
		}
	}
});