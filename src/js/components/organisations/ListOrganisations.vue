<template>
    <div>
        <div v-for="organisation in organisationResults" class="row">
            <div class="organisation-details">
                <img v-if="organisation['fields']['organisation_profile_picture'] == ''"
                     src="/static/NearBeach/images/placeholder/product_tour.svg"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <img v-else
                     v-bind:src="organisation['fields']['organisation_profile_picture']"
                     alt="Stakeholder Logo"
                     class="organisation-image"
                >
                <div class="organisation-name">
                    <a v-bind:href="`/organisation_information/${organisation['pk']}/`">
                        {{organisation['fields']['organisation_name']}}
                    </a>
                </div>
                <div class="organisation-link">
                    <i data-feather="external-link"></i> Website:
                    <a v-bind:href="organisation['fields']['organisation_website']" target="_blank">
                        {{ organisation['fields']['organisation_website'] }}
                    </a>
                </div>
                <div class="organisation-email">
                    <i data-feather="mail"></i> Email:
                    <a v-bind:href="`mailto:${organisation['fields']['organisation_email']}`">
                        {{organisation['fields']['organisation_email']}}
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListOrganisations",
        props: [
            'organisationResults',
        ],
        methods: {

        }
    }
</script>

<style scoped>

</style>