<template>
    <div class="card">
        <div class="card-body">
            <h2>{{importVariables['header']}} Search Results</h2>
            <hr>

            <!-- TABLE OF DATA -->
            <table class="table">
                <thead>
                    <tr>
                        <td></td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="result in searchResults">
                        <td></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ListSearchResults",
        props: {
            importVariables: Object,
            //{header, }
            searchResults: Array,
        }
    }
</script>

<style scoped>

</style>