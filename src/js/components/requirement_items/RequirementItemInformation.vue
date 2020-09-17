<template>
    <div class="card">
        <div class="card-body">
            <h1>Requirement Item Information</h1>
            <br/>
            <a v-bind:href="`/requirement_information/${requirementItemResults[0]['fields']['requirement']}/`">
                Go Back to requirement
            </a>
            <hr>

            <div class="row">
                <!-- Description -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        Requirement Items should be detailed. They should only focus on one small section of the
                        requirement.
                    </p>
                </div>

                <!-- Requirement item information -->
                <div class="col-md-8" style="min-height: 610px;">

                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "RequirementItemInformation.vue",
        props: [
            'requirementItemResults',
            'organisationResults',
            'defaultStakeholderImage',
            'statusList',
            'typeList',
        ],
        data() {
            return {
                statusFixList: [],
                typeFixList: [],
            };
        },
        methods: {},
        mounted() {},
    }
</script>

<style scoped>

</style>