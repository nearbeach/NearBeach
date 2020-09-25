<template>
    <div class="card">
        <div class="card-body">
            <!-- The MENU Items -->
            <ul class="nav nav-tabs" id="misc_module_tabs" role="tablist">
                <!-- Organisation Contacts -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="organisation-contacts-tab"
                       data-toggle="tab"
                       href="#organisation-contacts"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Organisation Contacts
                    </a>
                </li>

                <!-- Document Uploads -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="document-uploads-tab"
                       data-toggle="tab"
                       href="#document-uploads"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Document Uploads
                    </a>
                </li>

                <!-- Associated Projects & Tasks -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="associated-objects-tab"
                       data-toggle="tab"
                       href="#associated-objects"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Associated Objects
                    </a>
                </li>

                <!-- Organisation Quotes -->
<!--                <li class="nav-item"-->
<!--                    role="presentation"-->
<!--                >-->
<!--                    <a class="nav-link"-->
<!--                       id="organisation-quotes-tab"-->
<!--                       data-toggle="tab"-->
<!--                       href="#organisation-quotes"-->
<!--                       role="tab"-->
<!--                       aria-controls="home"-->
<!--                       aria-selected="true">Organisation Quotes-->
<!--                    </a>-->
<!--                </li>-->

                <!-- Misc Modules -->
                <li class="nav-item"
                    role="presentation"
                >
                    <a class="nav-link"
                       id="misc-modules-tab"
                       data-toggle="tab"
                       href="#misc-modules"
                       role="tab"
                       aria-controls="home"
                       aria-selected="true">Misc
                    </a>
                </li>
            </ul>
            <hr>

            <!-- The Modules -->
            <div class="tab-content" id="misc_module_content">
                <div class="tab-pane fade show active"
                     id="organisation-contacts"
                     role="tabpanel"
                     aria-labelledby="home-tab"
                >
                    ORGANISATION CONTACTS
                </div>
                <div class="tab-pane fade"
                     id="document-uploads"
                     role="tabpanel"
                     aria-labelledby="profile-tab"
                >
                    <documents-module v-bind:destination="destination"
                                      v-bind:location-id="locationId"
                    ></documents-module>
                </div>
                <div class="tab-pane fade active"
                     id="associated-objects"
                     role="tabpanel"
                     aria-labelledby="profile-tab"
                >
                    Associated Objects
                </div>
                <div class="tab-pane fade" id="organisation-quotes" role="tabpanel" aria-labelledby="contact-tab">
                    Organisation Quotes
                </div>
                <div class="tab-pane fade" id="misc-modules" role="tabpanel" aria-labelledby="contact-tab">
                    <misc-module v-bind:destination="destination"
                                 v-bind:location-id="locationId"
                    ></misc-module>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "OrganisationModules",
        props: [
            'destination',
            'locationId',
        ]
    }
</script>

<style scoped>

</style>