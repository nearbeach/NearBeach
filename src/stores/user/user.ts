import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => ({
    state: () => {
        return {
            id: 0 as number,
            username: "" as string,
            first_name: "" as string,
            last_name: "" as string,
            email: "" as string,
            profile_picture: "" as string,
            profile_picture_path: "" as string,
        }
    }
}))