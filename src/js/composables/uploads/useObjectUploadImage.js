import { toValue } from "vue";

export function useObjectUploadImage(blobInfo, progress) {
    const value = toValue(blobInfo);

    //Create the form
    const data_to_send = new FormData();
    data_to_send.set("document", value.blob(), value.filename());
    data_to_send.set("document_description", value.filename());
    data_to_send.set("uuid", this.uuid);

    //Configuration for axios
    const config = {
        onUploadProgress: (progressEvent) => {
            //As the document gets uploaded - we want to update the upload Percentage
            progress(parseFloat(progressEvent.loaded) / parseFloat(progressEvent.total));
        },
    };

    return this.axios.post(
        `${this.rootUrl}documentation/new_object_upload/`,
        data_to_send,
        config
    ).then((response) => {
        //Just send the location to the success
        return `/private/${response.data[0].document_key_id}`;
    }).catch((error) => {
        this.$store.dispatch("newToast",{
            header: "Error uploading image",
            message: `Error uploading image. Error -> ${error}`,
            extra_classes: "bg-danger",
            delay: 0,
        });

        return "";
    });
}