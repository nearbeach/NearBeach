<template>
    <div class="card">
        <div class="card-body">
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- REQUIREMENT ITEMS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement'"
                >
                    <a class="nav-link"
                       id="requirement-item-tab"
                       data-toggle="tab"
                       href="#requirement-items"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Requirement Item</a>
                </li>

                <!-- REQUIREMENT LINKS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement' || destination=='requirement_item'"
                >
                    <a class="nav-link"
                       id="requirement-link-tab"
                       data-toggle="tab"
                       href="#requirement-links"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Links</a>
                </li>

                <!-- DOCUMENTS -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="documents-tab"
                       data-toggle="tab"
                       href="#documents"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Documents</a>
                </li>

                <!-- CUSTOMERS -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="customer-tab"
                       data-toggle="tab"
                       href="#customers"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Customers</a>
                </li>

                <!-- BUGS -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="bug-tab"
                       data-toggle="tab"
                       href="#bugs"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Bugs</a>
                </li>

                <!-- GROUPS AND USERS -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="group-and-user-tab"
                       data-toggle="tab"
                       href="#group-and-users"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Groups and Users</a>
                </li>

                <!-- MISC -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="misc-tab"
                       data-toggle="tab"
                       href="#misc"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Misc</a>
                </li>
            </ul>
            <hr>

            <div class="tab-content" id="misc_module_content">
                <div class="tab-pane fade show active" id="requirement-items" role="tabpanel" aria-labelledby="home-tab">
                    <requirement-items-module v-bind:location-id="locationId"
                    ></requirement-items-module>
                </div>
                <div class="tab-pane fade" id="requirement-links" role="tabpanel" aria-labelledby="profile-tab">
                    <requirement-links-module></requirement-links-module>
                </div>
                <div class="tab-pane fade" id="documents" role="tabpanel" aria-labelledby="contact-tab">
                </div>
                <div class="tab-pane fade" id="customers" role="tabpanel" aria-labelledby="contact-tab">
                </div>
                <div class="tab-pane fade" id="bugs" role="tabpanel" aria-labelledby="contact-tab">
                </div>
                <div class="tab-pane fade" id="group-and-users" role="tabpanel" aria-labelledby="contact-tab">
                </div>
                <div class="tab-pane fade" id="misc" role="tabpanel" aria-labelledby="contact-tab">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ParentModules",
        props: [
            'destination', //Which object we are looking at, i.e. requirement
            'groupList',
            'locationId', //The ID of the object we are looking at.
            'requirementItemResults',
        ],
        components: {},
        data() {
            return {}
        },
        methods: {},
    }
</script>

<style scoped>

</style>