import {defineStore} from 'pinia'
import axios from 'axios'
import type {maximumPermissionInterface} from "@/utils/interfaces/stores/MaximumPermissionInterface.ts";
import type {permissionDataInterface} from "@/utils/interfaces/stores/PermissionDataInterface.ts";

// Setup Axios Instance
const axiosInstance = axios.create({
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
});

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
            errorInformation: "",
            hasError: false,
            isLoaded: false,
            permissionData: [] as permissionDataInterface[] | null,
            maximumPermissions: {
                kanbanBoard: 0,
                project: 0,
                requestForChange: 0,
                requirement: 0,
                settings: 0,
                task: 0,
            } as maximumPermissionInterface,
        }
    },
    actions: {
        _getMaximumFieldValue(field: string): number {
            // If there is no data - no permissions
            if (this.permissionData === null || this.permissionData.length === 0) {
                console.log("Escape Condition 1");
                return 0;
            }

            // TODO - Look at implementing this as a reduce functionality
            let permission_result : number = 0;
            this.permissionData.forEach((item) => {
                //field as keyof typeof someObj
                let item_results = item[field as keyof typeof item];
                console.log("TYPE OF: ", typeof(item_results));
                if (typeof(item_results) !== "number") {
                    // Early return
                    return permission_result;
                }

                // Check the value
                console.log("Permission Result: ", permission_result, " | Item Result: ", item_results);
                console.log("CONDITION: ",permission_result < item_results);
                permission_result = permission_result < item_results ? item_results : permission_result;
            });

            // Fallback
            return permission_result;
        },
        _setMaximumPermissions(): void {
            this.maximumPermissions.kanbanBoard = this._getMaximumFieldValue("kanbanBoard");
            this.maximumPermissions.project = this._getMaximumFieldValue("project");
            this.maximumPermissions.requestForChange = this._getMaximumFieldValue("requestForChange");
            this.maximumPermissions.requirement = this._getMaximumFieldValue("requirement");
            this.maximumPermissions.settings = this._getMaximumFieldValue("settings");
            this.maximumPermissions.task = this._getMaximumFieldValue("task");
        },
        async fetchPermissionData() {
            try {
                await axiosInstance.get(
                    "/api/v1/user/permissions/",
                ).then(async (response) => {
                    // Update the permission data
                    this.permissionData = response.data;

                    // Process the permission data
                    this._setMaximumPermissions();

                    // Last step - tell the system it has loaded
                    this.isLoaded = true;
                }).catch(async (error) => {
                    // Tell frontend we have an error
                    this.hasError = true;

                    // Write error into message
                    this.errorInformation = `Fetching permission details failed: ${error}`;
                });
            } catch (error) {
                // Tell frontend we have an error
                this.hasError = true;

                // Write error into message
                this.errorInformation = `Fetching permission details failed: ${error}`;
            }
        }
    },
    getters: {
        getCurrentObjectPermissions: state => {
            state.currentObjectPermissions
        },
        getErrorInformation(): string {
            return this.errorInformation;
        },
        getMaximumPermissions: state => {
            state.maximumPermissions
        },
        getPermissionData: state => {
            state.permissionData
        },
        hasPermission: (state) => {
            return (object: string) => {
                if (object as keyof maximumPermissionInterface && object in state.maximumPermissions) {
                    const max_permission: number = state.maximumPermissions[object as keyof maximumPermissionInterface]
                    return max_permission > 0;
                }

                // Default
                return true;
            }
        },
    }
})