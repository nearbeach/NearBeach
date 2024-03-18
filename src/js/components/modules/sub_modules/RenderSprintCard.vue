<template>
	<div
		v-for="sprint in sprintResults"
		v-bind:key="sprint.sprint_id"
		class="row object-link"
	>
		<!-- Sprint ID + Sprint Name -->
		<div class="col-md-10 object-link--details">
			<a v-bind:href="`${this.rootUrl}sprint_information/${sprint.sprint_id}/`"
			   target="_blank"
			   rel="noopener noreferrer"
			>
				<div class="object-link--link">Sprint- {{ sprint.sprint_id }}</div>
				<div class="object-link--title">{{ sprint.sprint_name }}</div>
				<div class="object-link--link">
					Story Point Progression:
					{{ sprint.completed_story_points }} out of {{ sprint.total_story_points }}
				</div>
				<div class="object-link--link">
					Dates:
					{{ getNiceDate(sprint.sprint_start_date) }} till {{ getNiceDate(sprint.sprint_end_date) }}
				</div>
			</a>
		</div>

		<!-- Sprint Status -->
		<div class="col-md-2 object-link--status">
			<span>Sprint Status: </span>
			<span>
				{{ sprint.sprint_status }}
			</span>
		</div>

		<!-- Object Delete -->
		<div
			class="object-link--remove"
			v-if="userLevel >= 2 && canDelete === true"
		>
			<Icon
				v-bind:icon="icons.trashCan"
				v-on:click="confirmRemoveSprintFunction(sprint)"
			/>
		</div>
	</div>
</template>

<script>
//Mixins
import datetimeMixin from "../../../mixins/datetimeMixin";
import iconMixin from "../../../mixins/iconMixin";

//Vuex
import { mapGetters } from "vuex";
import {Icon} from "@iconify/vue";

export default {
	name: "RenderSprintCard",
	components: {Icon},
	props: {
		canDelete: {
			type: Boolean,
			default: true,
		},
		sprintResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		})
	},
	mixins: [
		datetimeMixin,
		iconMixin,
	],
	emits: [
		"confirm_remove_sprint",
	],
	methods: {
		confirmRemoveSprintFunction(sprint) {
			//Send request upstream
			this.$emit("confirm_remove_sprint", sprint);
		}
	},
}
</script>