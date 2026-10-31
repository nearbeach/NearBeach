import { beforeEach, describe, expect, test } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import {NoteList} from ".";
import { createPinia, setActivePinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/router.ts";
import { nextTick } from "vue";
import i18n from "@/i18n.ts";
import { type NoteItemInterface } from "@/utils/interfaces/NoteItemInterface.ts";
import {PencilIcon, TrashIcon} from "@lucide/vue";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

describe("NoteList", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  test("renders note list when notes are provided", async () => {
    const notes: NoteItemInterface[] = [
      {
        id: 1,
        note: "Note 1",
        can_edit: true,
        date_modified: new Date(),
        first_name: "John",
        last_name: "Doe",
        profile_picture: "profile1.jpg",
        username: 1,
      },
      {
        id: 2,
        note: "Note 2",
        can_edit: true,
        date_modified: new Date(),
        first_name: "Jane",
        last_name: "Smith",
        profile_picture: "profile2.jpg",
        username: 2,
      },
    ];

    const wrapper = mount(NoteList, {
      props: {
        noteList: notes,
      },
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const noteItems = wrapper.findAll(".note-item");
    expect(noteItems.length).toBe(notes.length);

    noteItems.forEach((noteItem, index) => {
      const note = notes[index];
      expect(noteItem.find(".name").text()).toBe(`${note.first_name} ${note.last_name}`);
      expect(noteItem.find(".last-modified strong").text()).toBe("Last Modified:");
      // The date is rendered as-is, without any formatting
      expect(noteItem.find(".last-modified").text()).toContain(String(note.date_modified));
      expect(noteItem.find(".note-content").text()).toBe(note.note);
    });
  });

  test("emits deleteNote event when delete icon is clicked", async () => {
    const notes: NoteItemInterface[] = [
      {
        id: 1,
        note: "Note 1",
        can_edit: true,
        date_modified: new Date(),
        first_name: "John",
        last_name: "Doe",
        profile_picture: "profile1.jpg",
        username: 1,
      },
    ];

    const wrapper = mount(NoteList, {
      props: {
        noteList: notes,
      },
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const deleteIcon = wrapper.findComponent(TrashIcon);
    await deleteIcon.trigger("click");

    expect(wrapper.emitted().deleteNote).toBeTruthy();
    expect(wrapper.emitted().deleteNote[0]).toEqual([1]);
  });

  test("emits editNote event when edit icon is clicked", async () => {
    const notes: NoteItemInterface[] = [
      {
        id: 1,
        note: "Note 1",
        can_edit: true,
        date_modified: new Date(),
        first_name: "John",
        last_name: "Doe",
        profile_picture: "profile1.jpg",
        username: 1,
      },
    ];

    const wrapper = mount(NoteList, {
      props: {
        noteList: notes,
      },
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const editIcon = wrapper.findComponent(PencilIcon);
    await editIcon.trigger("click");

    expect(wrapper.emitted().editNote).toBeTruthy();
    expect(wrapper.emitted().editNote[0]).toEqual([0]);
  });

  test("renders empty message when no notes are provided", async () => {
    const wrapper = mount(NoteList, {
      props: {
        noteList: [],
      },
      global: {
        plugins: [i18n],
      },
    });

    await flushPromises();
    await nextTick();

    const emptyMessage = wrapper.find(".empty-note-list");
    expect(emptyMessage.exists()).toBe(true);
    expect(emptyMessage.text()).toBe("No notes in object");
    expect(wrapper.find(".note-list").exists()).toBe(false);
  });
});