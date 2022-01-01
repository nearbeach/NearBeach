<template>
    <div>
        <div v-for="organisation in organisationResults" 
             :key="organisation.id"
             class="row"
        >
            <div class="organisation-details">
                <img v-if="organisation['fields']['organisation_profile_picture'] == ''"
                     v-bind:src="`${staticUrl}/NearBeach/images/placeholder/product_tour.svg`"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <img v-else
                     v-bind:src="organisation['fields']['organisation_profile_picture']"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <div class="organisation-name">
                    <a v-bind:href="`${rootUrl}organisation_information/${organisation['pk']}/`">
                        {{organisation['fields']['organisation_name']}}
                    </a>
                </div>
                <div class="organisation-link">
                    <IconifyIcon v-bind:icon="icons.linkOut"></IconifyIcon> Website:
                    <a v-bind:href="organisation['fields']['organisation_website']" 
                       target="_blank"
                       rel="noopener noreferrer"
                    >
                        {{ organisation['fields']['organisation_website'] }}
                    </a>
                </div>
                <div class="organisation-email">
                    <IconifyIcon v-bind:icon="icons.mailIcon"></IconifyIcon> Email:
                    <a v-bind:href="`mailto:${organisation['fields']['organisation_email']}`">
                        {{organisation['fields']['organisation_email']}}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: "ListOrganisations",
        props: {
            organisationResults: {
                type: Array,
                default: () => {
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
            iconMixin,
        ],
        methods: {

        }
    }
</script>

<style scoped>

</style>
