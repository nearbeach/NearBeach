import { beforeEach, describe, expect, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useUserStore } from "@/stores/user/user.ts";

describe("User store", () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    test("starts with empty defaults", () => {
        const userStore = useUserStore();

        expect(userStore.id).toBe(0);
        expect(userStore.username).toBe("");
        expect(userStore.first_name).toBe("");
        expect(userStore.last_name).toBe("");
        expect(userStore.email).toBe("");
        expect(userStore.profile_picture).toBe("");
        expect(userStore.profile_picture_path).toBe("");
    });

    test("$patch stores the user's details", () => {
        const userStore = useUserStore();

        userStore.$patch({
            id: 11,
            username: "luke",
            first_name: "Luke",
            last_name: "Skywalker",
            email: "luke@example.com",
            profile_picture: "pic.png",
            profile_picture_path: "/media/pic.png",
        });

        expect(userStore.id).toBe(11);
        expect(userStore.username).toBe("luke");
        expect(userStore.first_name).toBe("Luke");
        expect(userStore.last_name).toBe("Skywalker");
        expect(userStore.email).toBe("luke@example.com");
        expect(userStore.profile_picture).toBe("pic.png");
        expect(userStore.profile_picture_path).toBe("/media/pic.png");
    });
});
