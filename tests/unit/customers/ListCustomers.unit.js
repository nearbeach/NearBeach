// Vitest
import { describe, expect, test } from "vitest";
import { mount } from "@vue/test-utils";

// Import vue component
import ListCustomers from "/src/js/components/customers/ListCustomers.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('ListCustomers.vue - list two customers', () => {
    //Using mount - insert data
    const wrapper = mount(ListCustomers, {
        props: {
            customerResults: [
                {
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
                },
                {
                    "model":"NearBeach.customer",
                    "pk":2,
                    "fields":{
                        "customer_title":2,
                        "customer_first_name":"Toby",
                        "customer_last_name":"Tripod",
                        "customer_email":"toby.tripod@nearbeach.org",
                        "customer_profile_picture":"",
                        "organisation":1,
                        "date_created":"2023-02-15T08:57:03.560Z",
                        "date_modified":"2023-07-15T07:16:58.841Z",
                        "change_user":1,
                        "is_deleted":false
                    }
                }
            ],
        },
        global: {
            plugins: [store]
        }
    });

    //Gather the list of customers rendered onto the page
    const customers = wrapper.findAll('.customer-details');

    test('customer 1 will have a custom profile picture', () => {
        const customer_1_profile = customers[0].find('.customer-image');

        //Check the image location
        expect(customer_1_profile.html()).toContain('<img src="/private/deb6dff2-74e6-4058-b30b-d7f4d015d2f0');
    });

    test('customer 2 will have the default profile picture', () => {
        const customer_2_profile = customers[1].find('.customer-image');

        //Check the image location
        expect(customer_2_profile.html()).toContain('<img src="/static/NearBeach/images/placeholder/product_tour.svg"');
    });

    test('both customer\'s names, emails, and hyperlinks are rendered out correctly', () => {
        const customer_1_name = customers[0].find('.customer-name');
        const customer_2_name = customers[1].find('.customer-name');

        //Check names
        expect(customer_1_name.text()).toEqual('Socks Fluffy');
        expect(customer_2_name.text()).toEqual('Toby Tripod');

        //Check hyperlinks
        expect(customer_1_name.html()).toContain('<a href="/customer_information/1/">');
        expect(customer_2_name.html()).toContain('<a href="/customer_information/2/">');
    });

    test('customer 1s email is rendered out correctly', () => {
        const customer_1_email = customers[0].find('.customer-email');
        const customer_2_email = customers[1].find('.customer-email');

        //Check email
        expect(customer_1_email.text()).toContain('socks@nearbeach.org');
        expect(customer_2_email.text()).toContain('toby.tripod@nearbeach.org');

        //Check hyperlinks
        expect(customer_1_email.html()).toContain('<a href="mailto:socks@nearbeach.org">');
        expect(customer_2_email.html()).toContain('<a href="mailto:toby.tripod@nearbeach.org">');
    });

    //We should also look at the "add customer" button. This should not render when the user does not have
    //enough permissions.
})
