export default {
    methods: {
        newObjectUploadImage(blobInfo, progress) {
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
            });
        },
        replaceIncorrectImageUrl(input_string) {
            //Using regex - we are finding the img src and removing the ../
            return input_string.replace(
                new RegExp("<img src=\"..\\/private\\/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\">"),
                (match) => {
                    return match.replace(
                        "../",
                        "/"
                    );
            })
        },
    },
};
