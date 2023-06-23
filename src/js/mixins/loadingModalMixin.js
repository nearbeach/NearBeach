import { Modal } from "bootstrap";

export default {
	methods: {
		closeLoadingModal() {
			//Get loader modal
			const loadingModal = new Modal(
				document.getElementById("loadingModal")
			);

			//Update the message in the loading modal
			document.getElementById(
				"loadingModalContent"
			).innerHTML = `UPDATED SUCCESSFULLY`;

			//Close after 1 second
			setTimeout(() => {
				loadingModal.hide();
			}, 1000);
		},
		showLoadingModal(destination) {
			//Open up the loading modal
			const loadingModal = new Modal(
				document.getElementById("loadingModal")
			);
			loadingModal.show();

			//Update message in loading modal
			document.getElementById(
				"loadingModalContent"
			).innerHTML = `Updating your ${destination} details`;
		},
	},
};
