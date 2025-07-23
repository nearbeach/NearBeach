<template>
    <div class="card">
        <div class="card-body">
            <h2>User API Keys</h2>
            <hr/>

            <div class="row">
                <div class="col-md-4">
                    <strong>User API Keys</strong>
                    <p class="text-instructions">
                        The following list is a list of all API keys for this user. You can delete or create any new
                        keys
                    </p>
                </div>
                <div class="col-md-8">
                    <div v-if="userApiKeyList.length === 0"
                         class="alert alert-info"
                    >
                        Currently there are no API keys for this user.
                    </div>
                    <div v-else>
                    	<table class="table">
							<thead>
								<tr>
									<td>Token</td>
									<td>Description</td>
									<td>Expiry</td>
									<td></td>
								</tr>
							</thead>
							<tbody>
								<tr v-for="api in userApiKeyList"
									:key="api.pk"
									:class="getRowClass(api.expiry)"
								>
									<td>{{ api.api_key }}</td>
									<td>{{ api.description }}</td>
									<td>{{ useNiceDatetime(api.expiry)}}</td>
									<td>
										<span
											class="remove-link"
										>
											<carbon-trash-can
												v-on:click="deleteUserApiKey(api.pk)"
											></carbon-trash-can>
										</span>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
                </div>
            </div>

            <hr/>
            <div class="row">
                <div class="col-md-12">
                    <button class="btn btn-primary save-changes"
                            v-on:click="openCreateUserApiKeyModal"
                    >
                        Create API Key
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div
		class="modal fade"
		id="createUserApiKeyModal"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Create API Key Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="createUserApiKeyModalCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Create User API Key</strong>
                            <p class="text-instructions">
                                Please fill out the description for the API Key. This will help you diffientiate where
                                the key will be utilised.
                            </p>
                            <p class="text-instructions">
                                Please specify if the API Key will expire.
                            </p>
						</div>
						<div class="col-md-8">
						    <div class="form-group">
                                <label for="api_description">
                                    API Description
                                </label>
                                <input id="api_description"
                                       v-model="apiDescription"
                                       type="text"
                                       class="form-control"
                                />
                            </div>
                            <div class="form-group">
                                <label for="api_expiry">Expiry</label>
                                <n-select v-model:value="apiExpiryModel"
                                          :options="expiryOptions"
                                ></n-select>

                            </div>
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
						v-on:click="createUserApiKey"
					>
						Create API Key
					</button>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
import {Modal} from "bootstrap";
import {NSelect} from "naive-ui";
import {mapGetters} from "vuex";
import {CarbonTrashCan} from "../../components";
import {useNiceDatetime} from "../../composables/datetime/useNiceDatetime";

export default {
    name: "UserApiList",
    props: {
        username: {
            type: Number,
            default: 0,
        },
    },
    components: {
		CarbonTrashCan,
        Modal,
        NSelect,
    },
    data() {
        return {
            apiDescription: "",
            apiExpiryModel: '30',
            expiryOptions: [
                { label: '30 Days', value: 30 },
                { label: '60 Days', value: 60 },
                { label: '90 Days', value: 90 },
                { label: '180 Days', value: 180 },
                { label: '365 Days', value: 365 },
                { label: 'Never', value: 'never' },
            ],
            userApiKeyList: [],
        }
    },
    computed: {
        ...mapGetters({
            rootUrl: "getRootUrl",
        })
    },
    methods: {
		useNiceDatetime,
        createUserApiKey() {
            const data_to_send = new FormData();
            data_to_send.append("description", this.apiDescription);

			// Handle the expiry date if required
			if (this.apiExpiryModel !== "never" && this.apiExpiryModel !== null && this.apiExpiryModel !== '') {
				data_to_send.append("expires_in", this.apiExpiryModel);
			}

            this.axios.post(
                `${this.rootUrl}api/v0/user/${this.username}/api_key/`,
                data_to_send,
            ).then((response) => {
                //Append data to user api key list
                this.userApiKeyList.push(response.data);

                //Close this modal
                document.getElementById("createUserApiKeyModalCloseButton").click();
            }).catch((error) => {
                this.$store.dispatch("newToast", {
                    header: "Error creating API Key",
                    message: `Sorry, we could not create the API Key. Error -> ${error}`,
                    extra_classes: "bg-danger",
                    delay: 0,
                });
            });
        },
        deleteUserApiKey(api_key_id) {
            this.axios.delete(
                `${this.rootUrl}api/v0/user/${this.username}/api_key/${api_key_id}/`,
            ).then(() => {
                this.userApiKeyList = this.userApiKeyList.filter(row => {
                    return row.pk !== api_key_id;
                });
            }).catch((error) => {
                this.$store.dispatch("newToast", {
                    header: "Error deleting API Key",
                    message: `Sorry, we could not delete the API Key. Error -> ${error}`,
                    extra_classes: "bg-danger",
                    delay: 0,
                });
            })
        },
		getRowClass(expiry) {
			if (expiry === null || expiry === "") return "";

			const expiry_date = new Date(expiry);
			const today_date = new Date();
			const difference = expiry_date.getTime() - today_date.getTime();

			if (difference <= 1000 * 60 * 60 * 24)
			{
				// The api key has expired, or is about to expire
				return "table-danger";
			}

			return "";
		},
        getUserApiKeys() {
            this.axios.get(
                `${this.rootUrl}api/v0/user/${this.username}/api_key/`,
            ).then((response) => {
                this.userApiKeyList = response.data;
            }).catch((error) => {
                this.$store.dispatch("newToast", {
                    header: "Error getting API Keys",
                    message: `Sorry, we could not get the API Keys. Error -> ${error}`,
                    extra_classes: "bg-danger",
                    delay: 0,
                });
            });
        },
        openCreateUserApiKeyModal() {
            const modal = new Modal(document.getElementById("createUserApiKeyModal"));
            modal.show();
        },
    },
    mounted() {
        //Load data
        this.getUserApiKeys();
    }

}
</script>