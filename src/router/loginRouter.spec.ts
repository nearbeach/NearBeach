import { afterEach, beforeEach, describe, expect, test } from "vitest";
import loginRouter, { loginRoutes } from "@/router/loginRouter.ts";

describe("loginRouter", () => {
    const originalUrl = window.location.href;

    beforeEach(async () => {
        await loginRouter.push("/login");
    });

    afterEach(() => {
        window.history.replaceState(null, "", originalUrl);
    });

    test("defines the login, forgotten password and reset password routes", () => {
        expect(loginRoutes.map((route) => route.name).filter(Boolean)).toEqual([
            "login",
            "forgotten-password",
            "password-reset",
        ]);
    });

    test.each([
        ["/login", "login"],
        ["/login/forgotten-password", "forgotten-password"],
        ["/login/reset-password", "password-reset"],
    ])("%s loads the %s page", async (path, name) => {
        await loginRouter.push(path);

        expect(loginRouter.currentRoute.value.name).toBe(name);
        expect(loginRouter.currentRoute.value.matched[0].components?.default).toBeTruthy();
    });

    test("unknown paths redirect to the login page", async () => {
        await loginRouter.push("/somewhere/else");

        expect(loginRouter.currentRoute.value.path).toBe("/login");
    });
});
