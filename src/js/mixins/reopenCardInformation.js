import {Modal} from "bootstrap";

export default {
    methods: {
        reopenCardInformation() {
            //This method will determine if we need to reopen the card information modal.
            let cardModal = document.getElementById("cardInformationModal");
            if (cardModal !== null)
            {
                cardModal = new Modal(cardModal);
                cardModal.show();
            }

            //Due to a bug with bootstrap, we have two divs with classes "modal-backdrop fade show"
            //Lets remove one of them
            setTimeout(() => {
                const div_modal = document.getElementsByClassName("modal-backdrop fade show");
                if (div_modal.length > 1) {
                    div_modal[0].remove();
                }
            }, 200);
        }
    }
}