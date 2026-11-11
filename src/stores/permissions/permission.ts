import {defineStore} from 'pinia'
import type {MaximumPermissionInterface} from "@/utils/interfaces/stores/MaximumPermissionInterface.ts";
import type {PermissionDataInterface} from "@/utils/interfaces/stores/PermissionDataInterface.ts";
import type {SelectOptionInterface} from "whelk-ui";
import type {TitleInterface} from "@/utils/interfaces/stores/TitleInterface.ts";

export const usePermissionStore = defineStore('permissions', {
    state: () => {
        return {
            currentObjectPermissions: {
                currentObject: 0,
                document: 0,
                kanban_note: 0,
                organisation_note: 0,
                project_note: 0,
                requirement_note: 0,
                requirement_item_note: 0,
                task_note: 0,
            },
            customerTitles: [] as TitleInterface[],
            errorInformation: "",
            hasAdministrationPermission: false,
            hasError: false,
            is_loaded: false,
            permissionData: [] as PermissionDataInterface[] | null,
            maximumPermissions: {
                administration_assign_user_to_group: 0,
                administration_create_group: 0,
                administration_create_permission_set: 0,
                administration_create_user: 0,
                kanban_board: 0,
                organisation: 0,
                project: 0,
                request_for_change: 0,
                requirement: 0,
                settings: 0,
                task: 0,
            } as MaximumPermissionInterface,
            userGroups: [] as SelectOptionInterface[],
        }
    },
    actions: {
        _getMaximumFieldValue(field: string): number {
            // If there is no data - no permissions
            if (this.permissionData === null || this.permissionData.length === 0) {
                return 0;
            }

            // TODO - Look at implementing this as a reduce functionality
            let permission_result = 0;
            this.permissionData.forEach((item: PermissionDataInterface) => {
                //field as keyof typeof someObj
                const item_results: number | string = item[field as keyof typeof item];
                if (typeof (item_results) === "number") {
                    permission_result = permission_result < item_results ? item_results : permission_result;
                }
            });

            // Fallback
            return permission_result;
        },
        _setHasAdministrationPermission(): void {
            this.hasAdministrationPermission = this.maximumPermissions.administration_assign_user_to_group
                + this.maximumPermissions.administration_create_group
                + this.maximumPermissions.administration_create_permission_set
                + this.maximumPermissions.administration_create_user
                > 0;
        },
        _setMaximumPermissions(): void {
            this.maximumPermissions.administration_assign_user_to_group = this._getMaximumFieldValue("administration_assign_user_to_group");
            this.maximumPermissions.administration_create_group = this._getMaximumFieldValue("administration_create_group");
            this.maximumPermissions.administration_create_permission_set = this._getMaximumFieldValue("administration_create_permission_set");
            this.maximumPermissions.administration_create_user = this._getMaximumFieldValue("administration_create_user");
            this.maximumPermissions.kanban_board = this._getMaximumFieldValue("kanban_board");
            this.maximumPermissions.project = this._getMaximumFieldValue("project");
            this.maximumPermissions.request_for_change = this._getMaximumFieldValue("request_for_change");
            this.maximumPermissions.requirement = this._getMaximumFieldValue("requirement");
            this.maximumPermissions.settings = this._getMaximumFieldValue("settings");
            this.maximumPermissions.task = this._getMaximumFieldValue("task");
            this.maximumPermissions.organisation = this._getMaximumFieldValue("organisation");
        },
        _setUserGroups(): void {
            const user_groups = this.permissionData?.map((item: PermissionDataInterface) => {
                return {
                    value: item.group_id.toString(),
                    label: item.group_name,
                    optGroup: "",
                } as SelectOptionInterface;
            });

            // Set the user groups
            this.userGroups = user_groups === undefined ? [] : user_groups;
        },
        processPermissionData() {
            this._setMaximumPermissions();
            this._setHasAdministrationPermission();
            this._setUserGroups();

            // State is loaded
            this.is_loaded = true;
        },
        SetCurrentObjectPermissions(destination: string, current_group_ids: Set<number>): void {
            // Making sure the destination exists in the maximum permissions
            const allowed_destinations = ["kanban_board", "project", "requirement", "task"];

            // If the destination is not allowed, return
            if (allowed_destinations.indexOf(destination) < 0) {
                // Default to 0
                this.currentObjectPermissions.currentObject = 0;
                return;
            }

            // Filter and reduce to get the data we want
            this.currentObjectPermissions.currentObject =
                this.permissionData?.filter((item: PermissionDataInterface) => {
                    // Filter for only the group we want
                    return current_group_ids.has(item.group_id);
                }).reduce((max: number, item) => {
                    // Get the new value (make sure destination is a keyof typeof item - default 0
                    const value = item[
                        destination as keyof typeof item
                        ] as number ?? 0;

                    // Return the max value
                    return value > max ? value : max;
                }, 0) ?? 0; // Default 0 in case everything breaks
        },
    },
    getters: {
        getCurrentObjectPermissions: state => {
            return state.currentObjectPermissions;
        },
        getErrorInformation(): string {
            return this.errorInformation;
        },
        getMaximumPermissions: state => {
            return state.maximumPermissions;
        },
        getPermissionData: state => {
            return state.permissionData;
        },
        getUserGroups: state => {
            return state.userGroups;
        },
        hasPermission: (state) => {
            return (object: string) => {
                if (object as keyof MaximumPermissionInterface && object in state.maximumPermissions) {
                    const max_permission: number = state.maximumPermissions[object as keyof MaximumPermissionInterface]
                    return max_permission > 0;
                }

                // Default
                return true;
            }
        },
    }
})