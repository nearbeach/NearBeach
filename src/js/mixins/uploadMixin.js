//Axios
import axios from "axios";

//VueX
import {mapGetters} from "vuex";

//Import Mixins
import errorModalMixin from "./errorModalMixin";

export default {
    computed: {
        ...mapGetters({
            destination: "getDestination",
            locationId: "getLocationId",
            rootUrl: "getRootUrl",
        }),
    },
    mixins: [errorModalMixin],
    methods: {
        uploadImage(blobInfo, progress) {
            //Create the form
            const data_to_send = new FormData();
            data_to_send.set("document", blobInfo.blob(), blobInfo.filename());
            data_to_send.set("document_description", blobInfo.filename());

            //Configuration for axios
            const config = {
                onUploadProgress: (progressEvent) => {
                    //As the document gets uploaded - we want to update the upload Percentage
                    progress =
                        parseFloat(progressEvent.loaded) /
                        parseFloat(progressEvent.total);
                },
            };

            //Use axios to send the data
            return axios
                .post(
                    `${this.rootUrl}documentation/${this.destination}/${this.locationId}/upload/`,
                    data_to_send,
                    config
                )
                .then((response) => {
                    //Just send the location to the success
                    return `/private/${response.data[0].document_key_id}`;
                })
                .catch((error) => {
                    this.showErrorModal(
                        error,
                        "Upload Image",
                        ""
                    );


                });
        },
        newObjectUploadImage(blobInfo, progress) {
            console.log("UUID: ", this.uuid);

            //Create the form
            const data_to_send = new FormData();
            data_to_send.set("document", blobInfo.blob(), blobInfo.filename());
            data_to_send.set("document_description", blobInfo.filename());
            data_to_send.set("uuid", this.uuid);

            //Configuration for axios
            const config = {
                onUploadProgress: (progressEvent) => {
                    //As the document gets uploaded - we want to update the upload Percentage
                    progress =
                        parseFloat(progressEvent.loaded) /
                        parseFloat(progressEvent.total);
                },
            };

            //Use axios to send the data
            return axios
                .post(
                    `${this.rootUrl}documentation/new_object_upload/`,
                    data_to_send,
                    config
                )
                .then((response) => {
                    //Just send the location to the success
                    return `/private/${response.data[0].document_key_id}`;
                })
                .catch((error) => {
                    this.showErrorModal(
                        error,
                        "Upload Image",
                        ""
                    );


                });
        }
    },
};
