<template>
	<div
		v-for="sprint in sprintResults"
		:key="sprint.sprint_id"
		class="row object-link"
	>
		<!-- Sprint ID + Sprint Name -->
		<div class="col-md-10 object-link--details">
			<a
:href="`${rootUrl}sprint_information/${sprint.sprint_id}/`"
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
					{{ useNiceDate(sprint.sprint_start_date) }} till {{ useNiceDate(sprint.sprint_end_date) }}
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
			v-if="userLevel >= 2 && canDelete === true"
			class="object-link--remove"
		>
			<carbon-trash-can
				@click="confirmRemoveSprintFunction(sprint)"
			></carbon-trash-can>
		</div>
	</div>
</template>

<script>
//Vuex
import { mapGetters } from "vuex";
import {CarbonTrashCan} from "../../../components";

//Composables
import {useNiceDate} from "Composables/datetime/useNiceDate";

export default {
	name: "RenderSprintCard",
	components: {CarbonTrashCan},
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
	emits: [
		"confirm_remove_sprint",
	],
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		})
	},
	methods: {
		useNiceDate,
		confirmRemoveSprintFunction(sprint) {
			//Send request upstream
			this.$emit("confirm_remove_sprint", sprint);
		}
	},
}
</script>