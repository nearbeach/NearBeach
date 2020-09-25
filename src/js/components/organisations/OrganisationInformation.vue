<template>
    <div class="card">
        <div class="card-body">
            <!-- TITLE -->
            <h1>Organisation Information</h1>
            <hr>

            <!-- FIELDS SECTION -->
            <div class="row">
                <div class="col-md-4">
                    <strong>Please Note</strong>
                    <p class="text-instructions">
                        Please only use generic information for both the website and email. Do not use any personal
                        details - you can create contacts in the section below.
                    </p>
                </div>
                <div class="col-md-3">
                    <img src="/static/NearBeach/images/placeholder/product_tour.svg"
                         alt="No Profile Picture"
                         class="organisation-profile-image"
                    />
                    <br/>
                    <button class="btn btn-primary">Update Profile...</button>
                </div>
                <div class="col-md-5">
                    <!-- ORGANISATION NAME -->
                    <div class="form-group">
                        <label for="id_organisation_name">Organisation Name</label>
                        <input id="id_organisation_name"
                               v-model="organisationNameModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION WEBSITE -->
                    <div class="form-group">
                        <label for="id_organisation_website">Organisation Website</label>
                        <input id="id_organisation_website"
                               v-model="organisationWebsiteModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- ORGANISATION EMAIL -->
                    <div class="form-group">
                        <label for="id_organisation_email">Organisation Email</label>
                        <input id="id_organisation_email"
                               v-model="organisationEmailModel"
                               type="text"
                               class="form-control"
                        >
                    </div>
                </div>
            </div>
            <br/>

            <!-- NEED TO APPLY PERMISSIONS -->
            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateOrganisation"
                    >Update Organisation</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "OrganisationInformation",
        props: [
            'organisationResults',
        ],
        data() {
            return {
                organisationNameModel: this.organisationResults[0]['fields']['organisation_name'],
                organisationEmailModel: this.organisationResults[0]['fields']['organisation_email'],
                organisationWebsiteModel: this.organisationResults[0]['fields']['organisation_website'],
            }
        },
        methods: {
            updateOrganisation: function() {

            },
        }
    }
</script>

<style scoped>

</style>