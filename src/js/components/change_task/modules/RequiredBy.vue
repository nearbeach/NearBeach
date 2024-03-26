<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Misc</strong>
			<p class="text-instructions">
				Please fill in the requiredBys for this particular
				change task. Default value will be "requiredBys".
			</p>
		</div>
		<div class="col-md-8">
			<div class="form-group">
				<label>Required By/Stakeholder:</label>
				<input
					type="text"
					class="form-control"
					v-model="requiredByModel"
				/>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "RequiredBy",
	computed: {
		requiredByModel: {
			get() {
				return this.$store.state.changeTask.requiredBy;
			},
			set(requiredBy) {
				//Update the VueX
				this.$store.commit({
					type: "updateChangeTaskRequiredBy",
					requiredBy: requiredBy,
				});

				//Destroy the first timer if it exists
				if (this.updateTimer !== "") {
					clearTimeout(this.updateTimer);
				}

				//Reset the timer
				this.updateTimer = setTimeout(() => {
					this.updateRequiredBy(requiredBy);
				}, 1200)
			},
		},
	},
	data() {
		return {
			updateTimer: "",
		}
	},
	methods: {
		updateRequiredBy(requiredBy) {
			this.$store.dispatch("newToast", {
				header: "Updating Required By",
				message: "Please wait, we are updating required by",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "required-save",
			});

			//Send to the backend
			const data_to_send = new FormData();
			data_to_send.set("change_task_required_by", requiredBy);

			this.axios.post(
				"update/required_by/",
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Required By",
					message: "The Required by has been updated",
					extra_classes: "bg-success",
					unique_type: "required-save",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Issue updating Required By",
					message: `We have had an issue updating required by. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "required-save",
				});
			})
		}
	}
}
</script>