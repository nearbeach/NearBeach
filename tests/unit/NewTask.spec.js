/**
 * @jest-environment jsdom
 */
import Vue from "vue";
import NewTask from "../../src/js/components/tasks/NewTask";

describe('NewTask', () => {
    //Make sure new-task loads
    test('NewTask - make sure it loads', () => {
        expect(true).toBe(true);
    })
});
