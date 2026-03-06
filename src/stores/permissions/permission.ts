import {defineStore} from 'pinia'
import axios from 'axios'

// Setup Axios Instance
const axiosInstance = axios.create({
    withCredentials: true,
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN",
});

// Interface
interface maximumPermissionInterface {
    kanbanBoard: number,
    project: number,
    requestForChange: number,
    requirement: number,
    settings: number,
    task: number,
}

interface permissionDataInterface {
    administration_assign_user_to_group: number,
    administration_create_group: number,
    administration_create_permission_set: number,
    administration_create_user: number,
    customer: number,
    document: number,
    group_id: number,
    group_name: string,
    kanban_board: number,
    organisation: number,
    organisation_note: number,
    project: number,
    project_note: number,
    request_for_change: number,
    requirement: number,
    requirement_item_note: number,
    requirement_note: number,
    schedule_object: number,
    sprint: number,
    task: number,
    tag: number,
    kanban_note: number,
    task_note: number,
}

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