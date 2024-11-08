<template>
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
			:key="result.pk"
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
						{{
							importVariables.prefix
						}}{{ result[importVariables.id] }}
					</p>
				</a>
			</td>
			<td>
				<!-- STATUS -->
				<p>{{ result[importVariables.status] }}</p>
				<div class="spacer"></div>
				<p class="small-text">
					{{ useNiceDatetime(result[importVariables.end_date]) }}
				</p>
			</td>
		</tr>
		</tbody>
	</table>
</template>

<script>

export default {
	name: "RenderObjectTable",
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
		rootUrl: {
			type: String,
			default: "/",
		},
		searchResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {};
	},
};
</script>
