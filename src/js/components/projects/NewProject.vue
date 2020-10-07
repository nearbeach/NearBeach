<template>
    <div class="card">
        <div class="card-body">
            <h1>New Project</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        To create a new project, fill out the form and submit at the bottom of the page.
                    </p>
                </div>

                <!-- PROJECT FORM -->
                <div class="col-md-8">
<!--                    <datetime v-model="dateModel"></datetime>-->
                    <div class="form-group">
                        <label>Project Name
<!--                            <span class="error" v-if="!$v.projectNameModel.required && $v.projectNameModel.$dirty"-->
<!--                            > Please suppy a title.</span>-->
                        </label>
                        <input type="text"
                               v-model="projectNameModel"
                               class="form-group"
                        >
                    </div>
                    <div class="form-group">
                        <between-dates destination="project"></between-dates>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "NewProject",
        data() {
            return {
                groupModel: {},
                projectDescriptionModel: '',
                projectEndDate: '',
                projectNameModel: '',
                projectStartDate: '',
                stakeholderOrganisation: {},
            }
        },
    }
</script>

<style scoped>

</style>