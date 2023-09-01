// ListCustomers.unit.js
import ListCustomers from "../../src/js/components/customers/ListCustomers.vue"

// Vitest
import { expect, test } from "vitest";


// it("testing GuessAge component props", async () => {
//   expect(GuessAge.props.title).toContain("Guess User Age App");
// });

test('list-customers', () => {
    const customer_1 = {
        "model":"NearBeach.customer",
        "pk":1,
        "fields":{
            "customer_title":2,
            "customer_first_name":"Socks",
            "customer_last_name":"Fluffy",
            "customer_email":"socks@nearbeach.org",
            "customer_profile_picture":"deb6dff2-74e6-4058-b30b-d7f4d015d2f0",
            "organisation":1,
            "date_created":"2023-02-15T08:57:03.560Z",
            "date_modified":"2023-07-15T07:16:58.841Z",
            "change_user":1,
            "is_deleted":false
        }
    }

    const customer_2 = {
        "model":"NearBeach.customer",
        "pk":1,
        "fields":{
            "customer_title":2,
            "customer_first_name":"Socks",
            "customer_last_name":"Fluffy",
            "customer_email":"socks@nearbeach.org",
            "customer_profile_picture":"",
            "organisation":1,
            "date_created":"2023-02-15T08:57:03.560Z",
            "date_modified":"2023-07-15T07:16:58.841Z",
            "change_user":1,
            "is_deleted":false
        }
    }

    test('profile_picture_shows', () => {
        expect(ListCustomers.methods.getProfilePicture(customer_1)).toBe("undefined/private/deb6dff2-74e6-4058-b30b-d7f4d015d2f0");
    });

});