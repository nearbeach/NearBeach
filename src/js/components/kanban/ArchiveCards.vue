<template>
    <div class="modal fade" 
         id="archiveCardsModal" 
         tabindex="-1" 
         data-bs-backdrop="static" 
         data-bs-keyboard="false" 
         aria-labelledby="exampleModalLabel" 
         aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Are you sure?</h5>
                    <button type="button" 
                            class="btn-close" 
                            data-bs-dismiss="modal" 
                            aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to archive the cards? This can not be undone.
                </div>
                <div class="modal-footer">
                    <button type="button" 
                            class="btn btn-secondary" 
                            data-bs-dismiss="modal"
                    >No</button>
                    <button type="button" 
                            class="btn btn-primary"
                    >Yes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { mapGetters } from 'vuex';
    import { Modal } from 'bootstrap';

    export default {
        name: "ArchiveCards",
        data() {
            return {
                archiveCardsModal: [],
            }
        },
        computed: {
            ...mapGetters({
                allCards: 'getCards',
                archiveDestination: 'getArchiveDestination',
                archiveDestinationString: 'getArchiveDestinationString',
            }),
        },
        watch: {
            archiveDestinationString(newValue) {
                //Check to make sure there are values within column or level
                if (newValue === undefined) return;
                
                //Open the modal
                this.archiveCardsModal = new Modal('#archiveCardsModal');
                this.archiveCardsModal.show();
            }
        },
        method: {
            archiveCards: function() {
                // //Simplify the variables
                // let column = this.archiveDestination.column;
                // let level = this.archiveDestination.level;

                // // Create data_to_send
                // const data_to_send = new FormData();

                // // Loop through the master list and get all card ids
                // // this.masterList.forEach(row => {
                // //     data_to_send.append('kanban_card_id', row['pk']);
                // // });
                // this.allCards.filter((card) => {
                //     return parseInt(card['fields']['kanban_column']) === column &&
                //         parseInt(card['fields']['kanban_level']) === level;
                // }).forEach((row) => {
                //     data_to_send.append('kanban_card_id', row['pk']);
                // })

                // //Mutate the data to exclude the archived cards
                // this.$store.commit({
                //     type: 'archiveCards',
                //     'column': this.columnId,
                //     'level': this.levelId,
                // });

                // // Use axios to contact backend
                // axios.post(
                //     `${this.rootUrl}kanban_information/archive_kanban_cards/`,
                //     data_to_send,
                // ).catch(error => {
                        
                // })
            }
        }
    }
</script>
