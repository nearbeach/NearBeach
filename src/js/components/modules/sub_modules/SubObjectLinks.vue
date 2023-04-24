<template>
    <h3 v-if="linkResults.length > 0">
        {{title}}
    </h3>
    <div v-for="link in linkResults"
            v-bind:key="link.pk"
            class="row object-link"
    >
        <!-- Object ID + Title -->
        <div class="col-md-10 object-link--details">
            <a v-bind:href="`${this.rootUrl}${link.object_type}_information/${link.object_id}/`" 
                target="_blank"
                rel="noopener noreferrer"
            >
                <div class="object-link--link">{{link.object_type}} - {{link.object_id}}</div>
                <div class="object-link--title">{{link.object_title}}</div>
            </a>
        </div>

        <!-- Object Status -->
        <div class="col-md-2 object-link--status">
            <span>Object Status: </span>
            <span>
                {{link.object_status}}
            </span>
        </div>

        <!-- Object Delete -->
        <div
            class="object-link--remove"
            v-if="userLevel >= 2"
        >
            <Icon
                v-bind:icon="icons.trashCan"
                v-on:click="removeLink(link)"
            />
        </div>
    </div>
    <div class="spacer-extra"
        v-if="linkResults.length > 0"
    ></div>
</template>

<script>
    import { mapGetters } from "vuex";
	import { Icon } from "@iconify/vue";
    const axios = require("axios");

	//Mixins
	import iconMixin from "../../../mixins/iconMixin";
    
    export default {
        name: "SubObjectLinks",
        components: {
            Icon,
        },
        mixins: [iconMixin],
        props: {
            linkResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            title: {
                type: String,
                default: "Relates",
            },
        },
        computed: {
            ...mapGetters({
                destination: "getDestination",
                locationId: "getLocationId",
                rootUrl: "getRootUrl",
                userLevel: "getUserLevel",
            }),
        },
        methods: {
            removeLink(link) {
				//Get the data to send into the backend
				let data_to_send = new FormData();
				data_to_send.set("link_id", link.object_id);
				data_to_send.set(
					"link_connection",
					link.object_type === this.destination ? "meta_object" : link.object_type
				);

				//Send the data to the backend
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_link/`,
						data_to_send
					)
					.then(() => {
						//Update the data
                        this.$emit("update_link_results");
					});
			},
        }
    }
</script>