<template>
    <div class="card">
        <div class="card-body">
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- GROUPS AND USERS -->
                <!-- Don't need to show to requirement items - as permissions are gained from parent requirement -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination!='requirement_item'"
                >
                    <button class="nav-link active"
                            id="group-and-user-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#group-and-users"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="true"
                    >Groups and Users</button>
                </li>

                <!-- REQUIREMENT ITEMS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement'"
                >
                    <button class="nav-link"
                            id="requirement-item-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#requirement-items"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Requirement Item</button>
                </li>

                <!-- REQUIREMENT LINKS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement'"
                >
                    <button class="nav-link"
                            id="requirement-link-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#requirement-links"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Requirement Links</button>
                </li>

                <!-- REQUIREMENT ITEM LINKS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination=='requirement_item'"
                >
                    <button class="nav-link"
                            id="requirement-item-link-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#requirement-item-links"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Links</button>
                </li>

                <!-- DOCUMENTS -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="documents-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#documents"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Documents</button>
                </li>

                <!-- LINKED OBJECTS -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination!=='requirement' && destination!=='requirement_item'"
                >
                    <button class="nav-link"
                            id="object-link-tabs"
                            data-bs-toggle="tab"
                            data-bs-target="#object-links"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Linked Objects</button>
                </li>

                <!-- CUSTOMERS -->
                <!-- Customers are not needed by requirement items as the parent requirements take care of this -->
                <li class="nav-item"
                    role="presentation"
                    v-if="destination!=='requirement_item'"
                >
                    <button class="nav-link"
                            id="customer-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#customers"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Customers</button>
                </li>

                <!-- BUGS -->
                <!-- This module will only appear for project, task, and requirement -->
                <li class="nav-item"
                    role="presentation"
                    v-if="['project','task','requirement'].includes(destination)"
                >
                    <button class="nav-link"
                            id="bug-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#bugs"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Bugs</button>
                </li>


                <!-- MISC -->
                <li class="nav-item"
                    role="presentation"
                >
                    <button class="nav-link"
                            id="misc-tab"
                            data-bs-toggle="tab"
                            data-bs-target="#misc"
                            type="button"
                            role="tab"
                            aria-controls="home"
                            aria-selected="false"
                    >Misc</button>
                </li>
            </ul>
            <hr>

            <div class="tab-content" id="misc_module_content">
                <div class="tab-pane fade show active" id="group-and-users" role="tabpanel" aria-labelledby="contact-tab">
                    <groups-and-users-module v-bind:location-id="locationId"
                                             v-bind:destination="destination"
                    ></groups-and-users-module>
                </div>
                <div class="tab-pane fade"
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
                <div class="tab-pane fade"
                     id="requirement-item-links"
                     role="tabpanel"
                     aria-labelledby="profile-tab"
                     v-else-if="destination=='requirement_item'"
                >
                    <requirement-item-links-module v-bind:location-id="locationId"
                                                   v-bind:destination="destination"
                    ></requirement-item-links-module>
                </div>

                <div class="tab-pane fade" id="documents" role="tabpanel" aria-labelledby="contact-tab">
                    <documents-module v-bind:location-id="locationId"
                                      v-bind:destination="destination"
                    ></documents-module>
                </div>
                <div class="tab-pane fade" id="object-links" role="tabpanel" aria-labelledby="contact-tab">
                    <object-links v-bind:destination="destination"
                                  v-bind:location-id="locationId"
                    ></object-links>
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
        props: {
            destination: String, //Which object we are looking at, i.e. requirement
            locationId: Number, //The ID of the object we are looking at.
            rootUrl: {
                type: String,
                default: '/',
            },
            staticUrl: {
                type: String,
                default: '/',
            },
        },
        data() {
            return {}
        },
        methods: {},
        mounted() {
            //Send data to required VueX states
            this.$store.commit({
                type: 'updateDestination',
                destination: this.destination,
                locationId: this.locationId,
            });
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            })
        }
    }
</script>

<style scoped>

</style>
