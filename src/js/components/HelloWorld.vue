<template>
    <h1>HELLO WORLD</h1>
</template>

<script>
export default {
    name: "HelloWorld",
    props: {
        input: {
            type: String,
            default: 'ERROR',
        }
    },
    mounted() {
        console.log("HELLO WORLD MOUNTED: ", this.input);
    }
}
</script>

<style scoped>

</style>