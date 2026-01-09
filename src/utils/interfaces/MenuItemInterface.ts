import type {Component} from "vue";

export interface MenuItemInterface {
    ariaLabel: string;
    destination: string;
    icon: Component;
    route: string;
    routeNew: string;
    title: string;
}
