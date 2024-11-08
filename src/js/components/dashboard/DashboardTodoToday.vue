<template>
	<div class="card"
		 v-if="todoList.length > 0"
	>
		<div class="card-body todays-todo">
			<h1 class="mb-4">Today's Todo</h1>
			<a v-bind:href="`${rootUrl}my_planner`">My Planner</a>
			<hr/>

			<div class="object-card-list">
				<div v-bind:class="`object-card ${ getExtraClasses(row.higher_order_status) }`"
					 v-for="row in todoList"
					 :key="row.user_job_id"
				>
					<div class="object-card--detail">
						<a v-bind:href="getUrl(row)">
							<div class="object-card--detail--link">
								{{ getPrefix(row.object_type) }}{{ row.location_id }}
							</div>
							<div class="object-card--detail--description">
								{{ row.title }}
							</div>
						</a>
					</div>
					<div class="object-card--status">
						<a v-bind:href="getUrl(row)">
							<div class="object-card--status--status">
								{{ row.status }}
							</div>
							<p class="small-text">
								{{ useNiceDatetime(row.end_date) }}
							</p>
						</a>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//Composables
import {useNiceDatetime} from "../../composables/datetime/useNiceDatetime";

export default {
	name: "DashboardTodoToday",
	components: {},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			todoList: [],
		}
	},
	methods: {
		useNiceDatetime,
		getExtraClasses(higher_order_status) {
			if (higher_order_status === "Closed") {
				return "bg-secondary-subtle";
			}

			return "";
		},
		getPrefix(data) {
			switch(data) {
				case "card":
					return "Card";
				case "project":
					return "Pro";
				case "task":
					return "Task";
				default:
					return "----";
			}
		},
		getTodoList() {
			//Use Axios to obtain data
			this.axios.post(
				`${this.rootUrl}dashboard/get/todo_today/`,
			).then((response) => {
				this.todoList = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Dashboard Data",
					message: `Can't get data for To Do Today. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});
		},
		getUrl(data) {
			return `${this.rootUrl}${data.object_type}_information/${data.location_id}/`;
		},
	},
	mounted() {
		this.getTodoList();
	}
}
</script>