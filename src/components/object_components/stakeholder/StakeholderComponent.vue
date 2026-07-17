<script setup lang="ts">
import StakeholderOrganisation
	from "@/components/object_components/stakeholder/stakeholder_organisation/StakeholderOrganisation.vue";
import StakeholderCustomer
	from "@/components/object_components/stakeholder/stakeholder_customer/StakeholderCustomer.vue";
import { WlkCard, WlkCardHeader} from "whelk-ui";

</script>

<template>
	<WlkCard class="stakeholder-component">
		<WlkCardHeader>
			<h3>Stakeholders</h3>
		</WlkCardHeader>

		<StakeholderOrganisation/>
		<StakeholderCustomer/>
	</WlkCard>
</template>

<style scoped>
.stakeholder-component {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}
}
</style>