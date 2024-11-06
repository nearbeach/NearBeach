import { toValue } from "vue";

export function useUploadImage(blobInfo) {
    const value = toValue(blobInfo);
    const rootUrl = this.$store.state.rootUrl;
    const destination = this.$store.state.destination;
    const locationId = this.$store.state.locationId;

    //Create the form
    const data_to_send = new FormData();
    data_to_send.set("document", value.blob(), value.filename());
    data_to_send.set("document_description", value.filename());

    //Use axios to send the data
    this.axios.post(
        `${rootUrl}documentation/${destination}/${locationId}/upload/`,
        data_to_send,
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