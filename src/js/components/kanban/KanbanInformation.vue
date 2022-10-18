<template>
    <div>
        <h1 class="kanban-header">{{kanbanBoardResults[0]['fields']['kanban_board_name']}}</h1>
        <a class="kanban-edit-text"
           v-if="userLevel >= 3"
           href="edit_board/"
        >
            Edit Kanban
        </a>
        <!-- Rendering the Kanban Container -->
        <kanban-board v-bind:column-results="columnResults"
                      v-bind:kanban-board-results="kanbanBoardResults"
                      v-bind:kanban-card-results="localKanbanCardResults"
                      v-bind:level-results="levelResults"
                      v-bind:new-card-info="newCardInfo"
                      v-on:double_clicked_card="doubleClickedCard($event)"
        ></kanban-board>

        <!-- MODALS -->
        <archive-cards></archive-cards>

        <new-kanban-card v-bind:kanban-card-results="kanbanCardResults"
                         v-bind:column-results="columnResults"
                         v-bind:level-results="levelResults"
                         v-bind:kanban-board-results="kanbanBoardResults"
                         v-on:new_card="newCard($event)"
        ></new-kanban-card>

        <card-information v-bind:card-information="cardInformation"
                          v-on:update_card="updateCard($event)"
        ></card-information>

        <new-kanban-link-wizard v-bind:location-id="locationId"
                                v-bind:column-results="columnResults"
                                v-bind:level-results="levelResults"
                                v-on:new_card="newCard($event)"
        ></new-kanban-link-wizard>

    </div>
</template>

<script>
    import { Modal } from "bootstrap";
    import ArchiveCards from "./ArchiveCards.vue"; 
    import KanbanBoard from "./KanbanBoard.vue";
    import NewKanbanCard from "../modules/wizards/NewKanbanCard.vue";
    import CardInformation from "../card_information/CardInformation.vue"
    import NewKanbanLinkWizard from "../modules/wizards/NewKanbanLinkWizard.vue";

    export default {
        name: "KanbanInformation",
        components: {
            ArchiveCards,
            CardInformation,
            KanbanBoard,
            NewKanbanCard,
            NewKanbanLinkWizard,
        },
        props: {
            columnResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            kanbanBoardResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            kanbanCardResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            levelResults: {
                type: Array,
                default: () => {
                    return [];
                }
            },
            locationId: {
                type: Number,
                default: 0,
            },
            rootUrl: {
                type: String,
                default: '/',
            },
            staticUrl: {
                type: String,
                default: '/',
            },
            userLevel: {
                type: Number,
                default: 0,
            },
        },
        data() {
            return {
                cardInformation: {},
                localKanbanCardResults: this.kanbanCardResults,
                newCardInfo: [],
            }
        },
        methods: {
            doubleClickedCard: function(data) {
                //Update the cardInformationId with the card id
                this.cardInformation = data;
            },
            newCard: function(data) {
                //this.newCardInfo = data;
                
                this.$store.commit({
                    type: 'addCard',
                    newCard: data,
                });
            },
            updateCard: function(data) {
                //Loop through the results - when the id's match. Update the data.
                this.localKanbanCardResults.forEach((row, index) => {
                    //Check to see if the primary keys match - if they do update the data
                    if (row['pk'] == data['kanban_card_id']) {
                        this.localKanbanCardResults[index]['fields']['kanban_card_text'] = data['kanban_card_text'];
                        this.localKanbanCardResults[index]['fields']['kanban_card_description'] = data['kanban_card_description'];
                        this.localKanbanCardResults[index]['fields']['kanban_column'] = data['kanban_column'];
                        this.localKanbanCardResults[index]['fields']['kanban_level'] = data['kanban_level'];
                    }
                }) 
            },
        },
        mounted() {
            //Send the urls upstream
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            });

            this.$store.commit({
                type: 'updateDestination',
                destination: "kanban_board",
                locationId: this.locationId,
            });

            //Send columns and levels into the VueX
            this.$store.commit({
                type: 'updateLists',
                'columnResults': this.columnResults,
                'levelResults': this.levelResults,
            })
        }
    }
</script>

<style scoped>

</style>
