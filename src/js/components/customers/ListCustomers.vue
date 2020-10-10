<template>
    <div>
        <div v-for="customer in customerResults" class="row">
            <div class="organisation-details">
                <img v-if="customer['fields']['customer_profile_picture'] == ''"
                     src="/static/NearBeach/images/placeholder/product_tour.svg"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <img v-else
                     v-bind:src="customer['fields']['customer_profile_picture']"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <div class="organisation-name">
                    <a v-bind:href="`/customer_information/${customer['pk']}/`">
                        {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                    </a>
                </div>
                <div class="organisation-email">
                    <i data-feather="mail"></i> Email:
                    <a v-bind:href="`mailto:${customer['fields']['customer_email']}`">
                        {{customer['fields']['customer_email']}}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListCustomers",
        props: [
            'customerResults',
        ],
        methods: {

        }
    }
</script>

<style scoped>

</style>