export default {
    methods: {
        getToken(TokenName) {
            //Use regex to extract out the require token
            const regEx = new RegExp(`${TokenName}=([^;]+)`);
            const value = regEx.exec(document.cookie);
            return value !== null ? encodeURIComponent(value[1]) : null;
        },
    },
};
