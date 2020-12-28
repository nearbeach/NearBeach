<template>
    <div class="card">
        <div class="card-body">
            <h1>New Request for Change</h1>
            <hr>

            <!-- FORM WIZARD -->
            <form-wizard @on-complete="onComplete"
                         title=""
                         subtitle=""
            >
                <!-- Description -->
                <tab-content title="Description">
                    <rfc-description></rfc-description>
                </tab-content>

                <!-- Details -->
                <tab-content title="Details">
                    <rfc-details v-bind:group-results="groupResults"
                                 v-bind:user-results="userResults"
                    ></rfc-details>
                </tab-content>

                <!-- Risk -->
                <tab-content title="Risk">
                    <rfc-risk></rfc-risk>
                </tab-content>

                <!-- Implementation Plan -->
                <tab-content title="Implementation Plan">
                    <rfc-implementation-plan></rfc-implementation-plan>
                </tab-content>

                <!-- Backout Plan -->
                <tab-content title="Backout Plan">
                    <rfc-backout-plan></rfc-backout-plan>
                </tab-content>

                <!-- Test Plan -->
                <tab-content title="Test Plan">
                    <rfc-test-plan></rfc-test-plan>
                </tab-content>
            </form-wizard>
        </div>
    </div>
</template>

<script>
    import {FormWizard, TabContent} from 'vue-form-wizard'
    import 'vue-form-wizard/dist/vue-form-wizard.min.css'

    export default {
        name: "NewRequestForChange",
        components: {
            FormWizard,
            TabContent
        },
        props: {
            groupResults: Array,
            userResults: Array,
        },
        methods: {
            onComplete: function() {},
        }
    }
</script>

<style scoped>

</style>