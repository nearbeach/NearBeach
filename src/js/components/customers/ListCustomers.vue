<template>
    <div>
        <div v-for="customer in customerResults" class="row">
            <div class="organisation-details">
                <img v-if="customer['fields']['customer_profile_picture'] == ''"
                     v-bind:src="`${staticUrl}/NearBeach/images/placeholder/product_tour.svg`"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <img v-else
                     v-bind:src="customer['fields']['customer_profile_picture']"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <div class="organisation-name">
                    <a v-bind:href="`${rootUrl}customer_information/${customer['pk']}/`">
                        {{customer['fields']['customer_first_name']}} {{customer['fields']['customer_last_name']}}
                    </a>
                </div>
                <div class="organisation-email">
                    <Icon v-bind:icon="icons.mailIcon"></Icon> Email:
                    <a v-bind:href="`mailto:${customer['fields']['customer_email']}`">
                        {{customer['fields']['customer_email']}}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //Mixin
    import iconMixin from "../../mixins/iconMixin";
    import { Icon } from '@iconify/vue';

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "ListCustomers",
        components: {
            Icon,
        },
        props: {
            customerResults: {
                type: Array,
                default: function() {
                    return [];
                },
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
                staticUrl: "getStaticUrl",
            }),
        },
        mixins: [
            iconMixin
        ],
    }
</script>

<style scoped>

</style>
