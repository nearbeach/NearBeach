<script setup lang="ts">
import { ref } from 'vue';
import CardComponent from "@/components/prefab/card/CardComponent.vue";
import CardHeader from "@/components/prefab/card/card_header/CardHeader.vue";
import StakeholderOrganisation
	from "@/components/project/project_page/stakeholder/stakeholder_organisation/StakeholderOrganisation.vue";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";
import StakeholderCustomer
	from "@/components/project/project_page/stakeholder/stakeholder_customer/StakeholderCustomer.vue";

// DEFINE REFS
const organisationName = ref<string>("Muenchener Rueckversicherungs Gesellschaft");
const organisationId = ref<number>(3);

// DEFINE METHODS
function removeOrganisation() {
	// Default the data for organisation
	organisationName.value = "";
	organisationId.value = 0;
}
</script>

<template>
	<CardComponent class="stakeholder-component">
		<CardHeader>
			<h3>Stakeholders</h3>
		</CardHeader>

		<StakeholderOrganisation
			v-if="organisationId !== 0"
			:organisation-name="organisationName"
			:organisation-id="organisationId"
			v-on:remove-organisation="removeOrganisation"
		/>
		<AddObject
			:object-type="ObjectTitleCaseEnums.organisation"
			v-else
		/>

		<StakeholderCustomer v-if="organisationId !== 0" />
	</CardComponent>
</template>

<style scoped>
.stakeholder-component {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}

	> .add-object {
		margin: 1rem 0;
	}
}

</style>