//Axios
import axios from "axios";

//VueX
import {mapGetters} from "vuex";

export default {
    computed: {
        ...mapGetters({
            destination: "getDestination",
            locationId: "getLocationId",
            rootUrl: "getRootUrl",
        }),
    },
    methods: {
        uploadImage(blobInfo) {
            //Create the form
            const data_to_send = new FormData();
            data_to_send.set("document", blobInfo.blob(), blobInfo.filename());
            data_to_send.set("document_description", blobInfo.filename());

            //Configuration for axios
            const config = {
                onUploadProgress: () => {
                    //As the document gets uploaded - we want to update the upload Percentage
                    
                },
            };

            //Use axios to send the data
            return this.axios.post(
                `${this.rootUrl}documentation/${this.destination}/${this.locationId}/upload/`,
                data_to_send,
                config
            ).then((response) => {
                //Just send the location to the success
                return `/private/${response.data[0].document_key_id}`;
            }).catch((error) => {
                this.$store.dispatch("newToast", {
                    header: "Failed to upload image",
                    message: `Sorry, could not upload image. Error -> ${error}`,
                    extra_classes: "bg-danger",
                    delay: 0,
                });
            });
        },
        newObjectUploadImage(blobInfo) {
            //Create the form
            const data_to_send = new FormData();
            data_to_send.set("document", blobInfo.blob(), blobInfo.filename());
            data_to_send.set("document_description", blobInfo.filename());
            data_to_send.set("uuid", this.uuid);

            //Configuration for axios
            const config = {
                onUploadProgress: () => {
                    //As the document gets uploaded - we want to update the upload Percentage
                    
                },
            };

            //Use axios to send the data
            return axios.post(
                `${this.rootUrl}documentation/new_object_upload/`,
                data_to_send,
                config
            ).then((response) => {
                //Just send the location to the success
                return `/private/${response.data[0].document_key_id}`;
            }).catch((error) => {
                this.$store.dispatch("newToast", {
                    header: "Failed to upload image",
                    message: `Sorry, could not upload image. Error -> ${error}`,
                    extra_classes: "bg-danger",
                    delay: 0,
                });
            });
        }
    },
};
