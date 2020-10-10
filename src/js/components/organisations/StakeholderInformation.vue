<template>
    <div class="row">
        <!-- Description -->
        <div class="col-md-4">
            <h2>Stakeholder</h2>
        </div>
        <div class="col-md-8 organisation-details">
            <img v-bind:src="getStakeholderImage" alt="Stakeholder Logo" class="organisation-image">
            <div class="organisation-name">
                {{stakeholderModel['organisation_name']}}
            </div>
            <div class="organisation-link">
                <i data-feather="external-link"></i> Website:
                <a v-bind:href="stakeholderModel['organisation_website']" target="_blank">
                    {{ stakeholderModel['organisation_website'] }}
                </a>
            </div>
            <div class="organisation-email">
                <i data-feather="mail"></i> Email:
                <a v-bind:href="`mailto:${stakeholderModel['organisation_email']}`">
                    {{stakeholderModel['organisation_email']}}
                </a>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "StakeholderInformation",
        props: {
            defaultStakeholderImage: String,
            organisationResults: Array
        },
        data() {
            return {
                stakeholderModel: this.organisationResults[0]['fields'],
            }
        },
        computed: {
            getStakeholderImage: function() {
                if (this.stakeholderModel['organisation_profile_picture'] == '') {
                    //There is no image - return the default image
                    return this.defaultStakeholderImage;
                }
                return this.stakeholderModel['organisation_profile_picture']
            }
        },
        methods: {

        },
    }
</script>

<style scoped>

</style>