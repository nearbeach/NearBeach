<template>
	<div class="card search-card">
		<div class="card-body">
			<h2>{{ importVariables.header }} Search Results</h2>
			<hr />

			<!-- TABLE OF DATA -->
			<table class="table">
				<thead>
					<tr>
						<td width="75%">{{ importVariables.header }}</td>
						<td width="25%">Status</td>
					</tr>
				</thead>
				<tbody>
					<tr
						v-for="result in searchResults"
						:key="result[importVariables.id]"
					>
						<td>
							<!-- LINK -->
							<a
								v-bind:href="`${rootUrl}${destination}_information/${
									result[importVariables.id]
								}/`"
							>
								<p>{{ result[importVariables.title] }}</p>
								<div class="spacer"></div>
								<p class="small-text">
									{{ importVariables.prefix
									}}{{ result[importVariables.id] }}
								</p>
							</a>
						</td>
						<td>
							<!-- STATUS -->
							{{ result[importVariables.status] }}
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script>
	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "ListSearchResults",
		props: {
			destination: {
				type: String,
				default: "",
			},
			importVariables: {
				type: Object,
				default: () => {
					return {
						header: "",
						prefix: "",
						id: 0,
						title: "",
						status: "",
					};
				},
			}, // {header, prefix,id, title, status}
			searchResults: {
				type: Array,
				default: () => {
					return [];
				},
			},
		},
		computed: {
			...mapGetters({
				rootUrl: "getRootUrl",
			}),
		},
	};
</script>

<style scoped></style>
