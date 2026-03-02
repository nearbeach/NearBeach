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

export const usePermissionStore = defineStore('permissions', {
    state: () => {
        return {
            maximumPermissions: {
                kanbanBoard: 0,
                project: 0,
                requestForChange: 0,
                requirement: 0,
                settings: 0,
                task: 0,
            } as maximumPermissionInterface,
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
            permissionData: [],
        }
    },
    actions: {
        _getMaximumFieldValue(field: string): number {
            if (this.permissionData.length === 0 ) {
                return 0;
            }

            // Reduce the function to get the maximum
            return this.permissionData.reduce(function(prev, curr) {
                return prev[field] > curr[field] ? prev : curr;
            });
        },
        _setMinimumPermissions(): void {
            this.maximumPermissions.kanbanBoard = this._getMaximumFieldValue("kanbanBoard");
            this.maximumPermissions.project = this._getMaximumFieldValue("project");
            this.maximumPermissions.requestForChange = this._getMaximumFieldValue("requestForChange");
            this.maximumPermissions.requirement = this._getMaximumFieldValue("requirement");
            this.maximumPermissions.settings = this._getMaximumFieldValue("settings");
            this.maximumPermissions.task = this._getMaximumFieldValue("task");
        },
        async fetchPermissionData() {
            try {
                axiosInstance.get(
                    "/api/v1/user/permissions/",
                ).then((response) => {
                    this.$state.permissionData = response.data;
                    this._setMinimumPermissions();
                }).catch((error) => {
                    // TODO - Implement the error method
                    console.error(error);
                })
            } catch (error) {
                // TODO - Implement error notifications
                console.error(error);
            }
        }
    },
    getters: {
        getMaximumPermissions: state => {
            state.maximumPermissions
        },
        getCurrentObjectPermissions: state => {
            state.currentObjectPermissions
        },
        getPermissionData: state => {
            state.permissionData
        },
    }
})