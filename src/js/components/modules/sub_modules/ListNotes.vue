<template>
    <div>
        <!-- NOTE HISTORY -->
        <div v-if="noteHistoryResults.length == 0"
             class="module-spacer"
        >
            <div class="alert alert-dark">
                Sorry - but there are no notes for this {{destination}}.
            </div>
        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <td>Note</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="noteHistory in noteHistoryResults">
                        <td>
                            <div>
                                <!-- This assumes that the object_note is always a single <p> tag -->
                                <p>{{noteHistory['fields']['object_note'].replace(/<p>|<\/p>/g, '').substr(0, 400)}}</p>
                            </div>
                            <div class="spacer"></div>
                            <p class="small-text">
                                {{noteHistory['fields']['date_created']}}
                            </p>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListNotes",
        props: {
            destination: String,
            noteHistoryResults: {
                type: Array,
                default: function() {
                    return [];
                },
            },
        }
    }
</script>

<style scoped>

</style>