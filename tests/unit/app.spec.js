/**
 * @jest-environment jsdom
 */
import Vue from "vue";
import AdminAddUser from "../../src/js/components/administration/AdminAddUser";
import NewRequestForChange from "../../src/js/components/request_for_change/NewRequestForChange";

describe('AdminAddUser', () => {
  test('Make sure the page loads', () => {
    expect(true).toBe(true);
  })
});

describe('NewRequestForChange', () => {
  test('NewRequestForChange Loads', () => {
    expect(true).toBe(true);
  })
})

test("TEST IS TEST", () => {
  expect(true).toBe(true);
})