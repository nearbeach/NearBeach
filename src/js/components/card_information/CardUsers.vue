<template>
    <div class="alert alert-secondary"
         v-if="userList.length === 0"
    >
        Sorry, there are no users currently assigned to this card.
    </div>
    <div v-else>
        <table class="table">
            <thead>
                <tr>
                    <td scope="col">Username</td>
                    <td scope="col">Name</td>
                    <td scope="col">Delete</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in userList"
                    v-bind:key="user.id"
                >
                    <td>{{user.id}}</td>
                    <td>{{user.first_name}} {{user.last_name}}</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="row" v-if="userLevel > 1">
        <div class="col-md-12">
            <button class="btn btn-primary"
                    v-on:click="addUser"
            >
                Add User
            </button>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { Modal } from "bootstrap";
    
    //Vuex components
    import { mapGetters } from "vuex";

    export default {
        name: "CardUsers",
        computed: {
            ...mapGetters({
                cardId: "getCardId",
                rootUrl: "getRootUrl",
                userLevel: "getUserLevel",
                userList: "getUserList",
            })
        },
        methods: {
            addUser: function() {
                //Close the current modal
                document.getElementById("cardInformationModalCloseButton").click();

                //Open the user wizard model
                const  addUserWizard = new Modal("#addUserModal");
                addUserWizard.show();
            },
        },
    }
</script>
