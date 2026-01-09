// stores/nav.ts
import { defineStore } from "pinia";

export const useNavStore = defineStore("nav", {
  state: () => {
    return {
      isNavOpen: false,
    };
  },
  actions: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    },
  },
});
