//Axios
import axios from "axios";
    
//VueX
import { mapGetters } from 'vuex';

export default {
    computed: {
        ...mapGetters({
            destination: "getDestination",
            locationId: "getLocationId",
            rootUrl: "getRootUrl",
        })
    },
    methods: {
        uploadImage: function(blobInfo, success, failure, progress) {
            
            //Create the form
            const data_to_send = new FormData();
            data_to_send.set('document', blobInfo.blob(), blobInfo.filename());
            data_to_send.set('document_description', blobInfo.filename());
                
            //Configuration for axios
            const config = {
                onUploadProgress: progressEvent => {
                    //As the document gets uploaded - we want to update the upload Percentage
                    progress = parseFloat(progressEvent.loaded) / parseFloat(progressEvent.total);
                }
            }
            
            //Use axios to send the data
            axios.post(
                `${this.rootUrl}documentation/${this.destination}/${this.locationId}/upload/`,
                data_to_send,
                config,
            ).then(response => {
                //Just send the location to the success
                success(`/private/${response.data[0].document_key_id}`);
            }).catch(error => {
                
                failure("Yeah, shit didn't work");
            })
            
        }
    }
}