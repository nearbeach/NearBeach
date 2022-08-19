import { Modal } from "bootstrap";

export default {
    methods: {
        closeLoadingModal: function() {
            //Get loader modal
            let loadingModal = new Modal(document.getElementById('loadingModal'));

            //Update the message in the loading modal
            document.getElementById("loadingModalContent").innerHTML = `UPDATED SUCCESSFULLY`;

            //Close after 1 second
            setTimeout(() => {
                loadingModal.hide();
            },1000)
        },
        showLoadingModal: function(destination) {
            //Open up the loading modal
            let loadingModal = new Modal(document.getElementById('loadingModal'));
            loadingModal.show();

            //Update message in loading modal
            document.getElementById("loadingModalContent").innerHTML = `Updating your ${destination} details`;
        },
    }
}