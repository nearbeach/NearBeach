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
                    v-if="destination=='requirement'"
                >
                    <a class="nav-link"
                       id="requirement-link-tab"
                       data-toggle="tab"
                       href="#requirement-links"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Links</a>
                </li>

                <!-- REQUIREMENT ITEM LINKS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement_item'"
                >
                    <a class="nav-link"
                       id="requirement-item-link-tab"
                       data-toggle="tab"
                       href="#requirement-item-links"
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
                <!-- Customers are not needed by requirement items as the parent requirements take care of this -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination!='requirement_item'"
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
                <!-- This module will only appear for project, task, and requirement -->
                <li class="nav-item"
                    role="presentation"
                    v-if="['project','task','requirement'].includes(destination)"
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
                <!-- Don't need to show to requirement items - as permissions are gained from parent requirement -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination!='requirement_item'"
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
                <div class="tab-pane fade show active"
                     id="requirement-items"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                     v-if="destination=='requirement'"
                >
                    <requirement-items-module v-bind:location-id="locationId"
                                              v-bind:destination="destination"
                    ></requirement-items-module>
                </div>
                <div class="tab-pane fade"
                     id="requirement-links"
                     role="tabpanel"
                     aria-labelledby="profile-tab"
                     v-if="destination=='requirement'"
                >
                    <requirement-links-module v-bind:location-id="locationId"
                                              v-bind:destination="destination"
                    ></requirement-links-module>
                </div>
                <div class="tab-pane fade active"
                     id="requirement-item-links"
                     role="tabpanel"
                     aria-labelledby="profile-tab"
                     v-else-if="destination=='requirement_item'"
                >
                    ADD CODE FOR REQUIREMENT ITEM LINKS!
                </div>

                <div class="tab-pane fade" id="documents" role="tabpanel" aria-labelledby="contact-tab">
                    <documents-module v-bind:location-id="locationId"
                                      v-bind:destination="destination"
                    ></documents-module>
                </div>
                <div class="tab-pane fade" id="customers" role="tabpanel" aria-labelledby="contact-tab">
                    <customers-module v-bind:location-id="locationId"
                                      v-bind:destination="destination"
                    ></customers-module>
                </div>
                <div class="tab-pane fade" id="bugs" role="tabpanel" aria-labelledby="contact-tab">
                    <bugs-module v-bind:location-id="locationId"
                                 v-bind:destination="destination"
                    ></bugs-module>
                </div>
                <div class="tab-pane fade" id="group-and-users" role="tabpanel" aria-labelledby="contact-tab">
                    <groups-and-users-module v-bind:location-id="locationId"
                                             v-bind:destination="destination"
                    ></groups-and-users-module>
                </div>
                <div class="tab-pane fade" id="misc" role="tabpanel" aria-labelledby="contact-tab">
                    <misc-module v-bind:location-id="locationId"
                                 v-bind:destination="destination"
                    ></misc-module>
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
        data() {
            return {}
        },
        methods: {},
    }
</script>

<style scoped>

</style>