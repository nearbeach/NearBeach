import { toValue } from "vue";

export function useUploadImage(blobInfo, progress) {
    const value = toValue(blobInfo);
    const rootUrl = this.$store.getters.getRootUrl;
    const destination = this.$store.getters.getDestination;
    const locationId = this.$store.getters.getLocationId;

    //Create the form
    const data_to_send = new FormData();
    data_to_send.set("document", value.blob(), value.filename());
    data_to_send.set("document_description", value.filename());

    //Configuration for axios
    const config = {
        onUploadProgress: (progressEvent) => {
            //As the document gets uploaded - we want to update the upload Percentage
            progress = parseFloat(progressEvent.loaded) / parseFloat(progressEvent.total);
        },
    };

    //Use axios to send the data
    return this.axios.post(
        `${rootUrl}documentation/${destination}/${locationId}/upload/`,
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