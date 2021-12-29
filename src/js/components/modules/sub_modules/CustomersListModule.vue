<template>
    <div class="customer-modules">
        <div v-for="customer in customerResults"
             :key="customer.pk"
             class="card card-customer"
        >
            <div class="card-body">
                <div class="single-customer-card"
                >
                    <img v-bind:src="getCustomerImage(customer)" alt="default profile picture" />
                    <div class="customer-card-name">
                        <a v-bind:href="`${rootUrl}customer_information/${customer.pk}/`">
                            {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                        </a>
                    </div>
                    <div class="customer-card-email">
                        <IconifyIcon v-bind:icon="icons.mailIcon"></IconifyIcon>
                        {{customer['fields']['customer_email']}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "CustomersListModule",
        props: [
            'customerResults',
        ],
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
            defaultCustomerImage: function() {
                return `${this.staticUrl}/NearBeach/images/placeholder/people_tax.svg`;
            }
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {}
        },
        methods: {
            getCustomerImage: function(customer) {
                if (customer['fields']['customer_profile_picture'] === '') {
                    //There is no image - return the default image
                    return this.defaultCustomerImage;
                }
                return customer['fields']['customer_profile_picture'];
            },
        },
    }
</script>

<style scoped>

</style>
