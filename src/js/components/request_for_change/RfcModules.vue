<template>
    <div class="card">
        <div class="card-body">
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- RISK -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-risk-tab"
                       data-toggle="tab"
                       href="#rfc-risk"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Risk</a>
                </li>

                <!-- IMPLEMENTATION -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-implementation-tab"
                       data-toggle="tab"
                       href="#rfc-implementation"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Implementation</a>
                </li>

                <!-- BACKOUT PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-backout-tab"
                       data-toggle="tab"
                       href="#rfc-backout"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Backout Plan</a>
                </li>

                <!-- TEST PLAN -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-test-plan-tab"
                       data-toggle="tab"
                       href="#rfc-test"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Test Plan</a>
                </li>

                <!-- RUN SHEET -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="rfc-run-sheet-tab"
                       data-toggle="tab"
                       href="#rfc-run-sheet"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Run Sheet</a>
                </li>
            </ul>
            <hr>

            <div class="tab-content" id="misc_module_content">
                <div class="tab-pane fade"
                     id="rfc-risk"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-risk></rfc-risk>
                </div>

                <div class="tab-pane fade"
                     id="rfc-implementation"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-implementation-plan></rfc-implementation-plan>
                </div>

                <div class="tab-pane fade"
                     id="rfc-backout"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-backout-plan></rfc-backout-plan>
                </div>

                <div class="tab-pane fade"
                     id="rfc-test"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    <rfc-backout-plan></rfc-backout-plan>
                </div>

                <div class="tab-pane fade"
                     id="rfc-run-sheet"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    PROGRAM THE RUN SHEET
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "RfcModules",
        props: {
            locationId: Number,
            destination: String,
        },
    }
</script>

<style scoped>

</style>