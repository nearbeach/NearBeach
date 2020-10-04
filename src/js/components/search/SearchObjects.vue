<template>
    <div>
        <div class="card">
            <div class="card-body">
                <!-- HEADING -->
                <h1>Search</h1>
                <hr>

                <!-- SEARCH FIELD -->
                <div class="form-row">
                    <div class="form-group">
                        <label>Search:</label>
                        <input type="text"
                               class="form-control search-organisation"
                               v-model="searchModel"
                        >
                    </div>
                    <div class="form-group">
                        <input type="checkbox"
                               id="inlcudeClosedObjects"
                               v-model="includeClosedObjectsModel"
                        >
                        <label for="inlcudeClosedObjects"> Include Closed Objects</label>
                    </div>
                </div>
            </div>
        </div>
        <br/>

        <!-- REQUIREMENTS RESULTS -->
        <div class="card">
            <div class="card-body">
                <h2>Requirement Search Results</h2>
                <hr>
                ADD CODE
            </div>
        </div>
        <br/>

        <!-- PROJECT RESULTS -->
        <div class="card">
            <div class="card-body">
                <h2>Project Search Results</h2>
                <hr>
                ADD CODE
            </div>
        </div>
        <br/>

        <!-- TASK RESULTS -->
        <div class="card">
            <div class="card-body">
                <h2>Task Search Results</h2>
                <hr>
                ADD CODE
            </div>
        </div>
        <br/>
    </div>
</template>

<script>
    export default {
        name: "SearchObjects",
        props: {
            includeClosed: {
                Boolean,
            },
            searchInput: {
                String,
                required: false,
            },
            searchResults: {
                Array,
                required: true,
            },
        },
        data() {
            return {
                includeClosedObjectsModel: this.includeClosed,
                searchModel: this.searchInput,
            }
        },
        methods: {

        },
        watch: {

        },
        mounted() {
            //If the include closed is undefined - then we want to define it
            if (this.includeClosed == undefined) {
                this.includeClosedObjectsModel = false;
            }
        }
    }
</script>

<style scoped>

</style>