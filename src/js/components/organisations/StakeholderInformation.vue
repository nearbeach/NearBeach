<template>
    <div class="row">
        <!-- Description -->
        <div class="col-md-4">
            <h2>Stakeholder</h2>
        </div>
        <div class="col-md-8 organisation-details">
            <img v-bind:src="getStakeholderImage" alt="Stakeholder Logo" class="organisation-image">
            <div class="organisation-name">
                <a v-bind:href="`/organisation_information/${organisationResults[0]['pk']}/`">
                    {{stakeholderModel['organisation_name']}}
                </a>
            </div>
            <div class="organisation-link">
                <IconifyIcon v-bind:icon="icons.linkOut"></IconifyIcon> Website:
                <a v-bind:href="stakeholderModel['organisation_website']" target="_blank">
                    {{ stakeholderModel['organisation_website'] }}
                </a>
            </div>
            <div class="organisation-email">
                <IconifyIcon v-bind:icon="icons.mailIcon"></IconifyIcon> Email:
                <a v-bind:href="`mailto:${stakeholderModel['organisation_email']}`">
                    {{stakeholderModel['organisation_email']}}
                </a>
            </div>
        </div>
    </div>
</template>

<script>
    //Import icons
    import linkOut from '@iconify-icons/akar-icons/link-out';
    import mailIcon from '@iconify-icons/fe/mail';

    export default {
        name: "StakeholderInformation",
        props: {
            defaultStakeholderImage: String,
            organisationResults: Array
        },
        data() {
            return {
                icons: {
                    linkOut: linkOut,
                    mailIcon: mailIcon,
                },
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