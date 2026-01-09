<script setup lang="ts"></script>

<template>
    <div class="playground">
        <div class="card-1 col-50"></div>
        <div class="card-2 col-50"></div>
        <div class="card-3 col-ms-50"></div>
        <div class="card-4 col-ms-50"></div>
    </div>
</template>

<style scoped>
.playground {
    display: flex;
    flex-direction: row;
    width: 75vw;
    min-height: 50vh;
    background-color: hotpink;
    flex-wrap: wrap;

    > div {
        min-height: 10px;
        width: 100%;

        @media (--small-screen) {
            &.col-25 {
                width: 25%;
            }

            &.col-33 {
                width: 33%;
            }

            &.col-50 {
                width: 50%;
            }

            &.col-66 {
                width: 66%;
            }

            &.col-75 {
                width: 75%;
            }
        }
        @media (--medium-screen) {
            &.col-ms-25 {
                width: 25%;
            }

            &.col-ms-33 {
                width: 33%;
            }

            &.col-ms-50 {
                width: 50%;
            }

            &.col-ms-66 {
                width: 66%;
            }

            &.col-ms-75 {
                width: 75%;
            }
        }
        @media (--large-screen) {
            &.col-ls-25 {
                width: 25%;
            }

            &.col-ls-33 {
                width: 33%;
            }

            &.col-ls-50 {
                width: 50%;
            }

            &.col-ls-66 {
                width: 66%;
            }

            &.col-ls-75 {
                width: 75%;
            }
        }
    }
}

.card-1 {
    background-color: skyblue;
}

.card-2 {
    background-color: brown;
}

.card-3 {
    background-color: blueviolet;
}

.card-4 {
    background-color: salmon;
}
</style>
