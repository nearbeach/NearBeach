<template>
	<div
		class="modal fade"
		id="newChangeTaskLinkModal"
		tabindex="-1"
		aria-labelledby="linkModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.linkOut"></Icon> New
						Change Task Link Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="linkCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<!-- CHOOSE RELATIONSHIP TYPE -->
					<div class="row">
						<div class="col-md-4">
							<strong>Relationship</strong>
							<p class="text-instructions">
								Please indicate if you are blocking future Changes Tasks, or if a
                                past Change Task is blocking current Change Task.
							</p>
						</div>
						<div class="col-md-8">
							Current change task <br />
							<n-select
								:options="changeTaskRelation"
								v-model:value="changeTaskRelationModel"
								class="object-selection"
							></n-select>
						</div>
					</div>
					<hr />

					<!-- SELECTING WHICH OBJECTS TO LINK TO -->
					<div class="row">
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the change tasks you want to
								connect to this change task.
							</p>
						</div>
						<div class="col-md-8">
							<div
								v-if="changeTaskResults.length === 0"
								class="alert alert-warning"
							>
								Sorry - there are no results.
							</div>

							TODO: ADD IN RENDER CONTENT
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-bind:disabled="linkModel.length == 0"
						v-on:click="saveLinks"
					>
						Save changes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
    const axios = require('axios');

	import iconMixin from "../../../mixins/iconMixin";
	import { Icon } from "@iconify/vue";
    import { NSelect } from "naive-ui";
    
    //VueX
	import { mapGetters } from "vuex";
    
    export default {
        name: "NewChangeTaskLinkWizard",
        components: {
            Icon,
            NSelect,
        },
        data() {
            return {
                changeTaskRelation: [
					{ value: "blocked_by", label: "Is Blocked By" },
					{ value: "blocking", label: "Is Currently Blocking" },
				],
				changeTaskRelationModel: "blocking",
				changeTaskResults: [],
                linkModel: [],
            }
        },  
        computed: {
			...mapGetters({
                destination: "getDestination",
                locationId: "getLocationId",
				rootUrl: "getRootUrl",
				staticUrl: "getStaticUrl",
			}),
		},
        mixins: [iconMixin],
        methods: {
            getAllChangeTasks() {
                //Use Axios to get data
                axios.post(
                    `${this.rootUrl}change_task_information/${this.locationId}/get_change_task_list/`
                ).then(response => {
                    this.changeTaskResults = response.data;
                })
            }
        },
        mounted() {
            //Get the required data
            setTimeout(()=> {
                this.getAllChangeTasks();
            }, 200);
        }
    }
</script>