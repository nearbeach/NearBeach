<template>
    <div>
        <div class="col-md-6">
            <div class="form-group">
                <label>{{destination}} Start Date:</label>
                <datetime type="datetime"
                          v-model="localStartDateModel"
                ></datetime>
            </div>
        </div>
        <div class="col-md-6">
            <div class="form-group">
                <label>{{destination}} End Date:</label>
                <datetime type="datetime"
                          v-model="localEndDateModel"
                ></datetime>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "BetweenDates",
        props: {
            destination: String,
            endDateModel: {
                Date,
                default: () => {
                    return new Date();
                },
            },
            startDateModel: {
                Date,
                default: () => {
                    return new Date();
                },
            },
        },
        data() {
            return {
                localEndDateModel: this.endDateModel,
                localStartDateModel: this.startDateModel,
            }
        }
    }
</script>

<style scoped>

</style>