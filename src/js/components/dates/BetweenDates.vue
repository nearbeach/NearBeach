<template>
    <div class="row">
        <div class="col-md-4">
            <strong>Between Dates</strong>
            <p class="text-instructions">
                Choose the start and end date of the {{destination}}. Please note the end date can not be earlier than
                the start date. They can be equal.
            </p>
        </div>
        <div class="col-md-4">
            <div class="form-group">
                <label>{{destination}} Start Date:
                    <span class="error"
                          v-if="!$v.localStartDateModel.required && isDirty"
                    > Please select a date.</span>
                </label>
                <datetime type="datetime"
                          v-model="localStartDateModel"
                          input-class="form-control"
                          v-bind:minute-step="5"
                ></datetime>
            </div>
        </div>
        <div class="col-md-4">
            <div class="form-group">
                <label>{{destination}} End Date:
                    <span class="error"
                          v-if="!$v.localEndDateModel.required && isDirty"
                    > Please select a date.</span>
                </label>
                <datetime type="datetime"
                          v-model="localEndDateModel"
                          input-class="form-control"
                          v-bind:minute-step="5"
                ></datetime>
            </div>
        </div>
    </div>
</template>

<script>
    import { DateTime } from "luxon";

    //Validation
    import { required } from 'vuelidate/lib/validators';

    export default {
        name: "BetweenDates",
        props: {
            destination: {
                type: String,
                default: "",
            },
            endDateModel: {
                type: [Object,String],
                default() {
                    //Define a date variable
                    var date = DateTime.local();

                    //Add 28 days (4 weeks) to the date
                    date = date.plus({ days: 28 })

                    //Return the data
                    return date;
                }
            },
            isDirty: Boolean,
            startDateModel: {
                type: [Object,String],
                default() {
                    //Just return today's date
                    return DateTime.local();
                }
            },
        },
        validations: {
            localEndDateModel: {
                required,
            },
            localStartDateModel: {
                required,
            },
        },
        data() {
            return {
                localEndDateModel: '',
                localStartDateModel: '',
            }
        },
        methods: {
            emitDates: function() {
                //Send this data upstream
                this.$emit('update_dates',{
                    'start_date': this.localStartDateModel,
                    'end_date': this.localEndDateModel
                })
            },
        },
        watch: {
            localEndDateModel: function() {
                var end_date = DateTime.local(this.localEndDateModel),
                    start_date = DateTime.local(this.localStartDateModel);

                //Makes sure the end date is not less than the start date - if it is, turn it into the start date
                if (end_date.toMillis() - start_date.toMillis() < 0) {
                    //The Start date is larger than the end date - make it the same
                    this.localEndDateModel = this.localStartDateModel();
                }

                //Send the new results up steam
                this.emitDates();
            },
            localStartDateModel: function() {
                var end_date = DateTime.local(this.localEndDateModel),
                    start_date = DateTime.local(this.localStartDateModel);

                //Makes sure the start date is not greater than the end date - if it is, turn it into the end date
                if (end_date.toMillis() - start_date.toMillis() < 0) {
                    //The Start date is larger than the end date - make it the same
                    this.localStartDateModel = this.localEndDateModel();
                }

                //Send the new results up stream
                this.emitDates();
            },
        },
        mounted() {
            //Update local variables with imported data
            this.localEndDateModel = this.endDateModel.toISO();
            this.localStartDateModel = this.startDateModel.toISO();
        }
    }
</script>

<style scoped>

</style>