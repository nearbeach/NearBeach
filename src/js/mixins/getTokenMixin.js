export default {
    methods: {
        getToken: function(TokenName) {
            //Use regex to extract out the require token
            let regEx = new RegExp(TokenName + "=([^;]+)");
            let value = regEx.exec(document.cookie);
            return (value !== null) ? encodeURIComponent(value[1]) : null;
        }
    }
}