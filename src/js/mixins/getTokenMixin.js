export default {
    methods: {
        getToken: function(TokenName) {
            //Use regex to extract out the require token
            var regEx = new RegExp(TokenName + "=([^;]+)");
            var value = regEx.exec(document.cookie);
            return (value != null) ? encodeURIComponent(value[1]) : null;
        }
    }
}