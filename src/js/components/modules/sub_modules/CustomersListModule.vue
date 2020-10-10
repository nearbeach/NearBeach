<template>
    <div class="customer-modules">
        <div v-for="customer in customerResults"
                 class="card card-customer"
        >
            <div class="card-body">
                <div class="single-customer-card">
                    <img v-bind:src="getCustomerImage(customer)" alt="default profile picture" />
                    <div class="customer-card-name">
                        {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                    </div>
                    <div class="customer-card-email"><i data-feather="email"></i>
                        {{customer['fields']['customer_email']}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CustomersListModule",
        props: [
            'customerResults',
        ],
        data() {
            return {
                defaultCustomerImage: '/static/NearBeach/images/placeholder/people_tax.svg',
            }
        },
        methods: {
            getCustomerImage: function(customer) {
                if (customer['fields']['customer_profile_picture'] == '') {
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