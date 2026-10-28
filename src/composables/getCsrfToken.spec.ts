import {afterEach, beforeEach, describe, expect, test} from "vitest";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

function clearCookies() {
	document.cookie.split(";").forEach((cookie) => {
		const name = cookie.split("=")[0].trim();
		if (name !== "") {
			document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
		}
	});
}

describe("getCsrfToken", () => {
	beforeEach(clearCookies);
	afterEach(clearCookies);

	test("returns an empty string when there is no csrf cookie", () => {
		expect(getCsrfToken()).toBe("");
	});

	test("returns the value of the csrftoken cookie", () => {
		document.cookie = "csrftoken=abc123; path=/";

		expect(getCsrfToken()).toBe("abc123");
	});

	test("finds the cookie among other cookies", () => {
		document.cookie = "theme=dark; path=/";
		document.cookie = "csrftoken=xyz789; path=/";
		document.cookie = "language=en; path=/";

		expect(getCsrfToken()).toBe("xyz789");
	});

	test("does not include the cookies that follow it", () => {
		document.cookie = "csrftoken=first; path=/";
		document.cookie = "sessionid=second; path=/";

		expect(getCsrfToken()).toBe("first");
	});

	test("keeps characters that are common in a token", () => {
		document.cookie = "csrftoken=Ab-Cd_Ef0123456789; path=/";

		expect(getCsrfToken()).toBe("Ab-Cd_Ef0123456789");
	});

	test("ignores a cookie that only ends in csrftoken", () => {
		document.cookie = "other_csrftoken=not-this-one; path=/";
		document.cookie = "csrftoken=this-one; path=/";

		expect(getCsrfToken()).toBe("this-one");
	});

	test("is an empty string when only a look-alike cookie exists", () => {
		document.cookie = "other_csrftoken=not-this-one; path=/";

		expect(getCsrfToken()).toBe("");
	});
});
