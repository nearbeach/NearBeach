export default {
  methods: {
    searchTrigger: function (obj) {
      //obj is an object passed through with references to the original sources. We will manipulate these sources

      //Reset the timer if it exists
      if (obj.searchTimeout != '') {
        //Stop the clock!
        clearTimeout(obj.searchTimeout);
      }

      // If the obj.search is defined, we want to use the search Defined. Otherwise search undefined
      if (obj.search === undefined) {
        this.searchUndefined(obj);
      } else {
        this.searchDefined(obj);
      }
    },
    searchDefined: function (obj) {
      // Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
      if (obj.search.length >= 3) {
        obj.searchTimeout = setTimeout(
          obj.return_function,
          500,
          obj.search,
          obj.loading
        );
      }
    },
    searchUndefined: function (obj) {
      // Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
      obj.searchTimeout = setTimeout(obj.return_function, 500);
    },
  },
};
