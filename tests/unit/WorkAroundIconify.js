/*
Due to an issue with JestJS, it causes the icon files to not compile in the vue templates. As a work around, we are
mocking the icons as blank functions.
 */
jest.mock('@iconify-icons/akar-icons/arrow-up', () => jest.fn());
jest.mock('@iconify/icons-akar-icons/bug', () => jest.fn());
jest.mock('@iconify-icons/bx/bx-briefcase', () => jest.fn());
jest.mock('@iconify/icons-bi/card-checklist', () => jest.fn());
jest.mock('@iconify/icons-feather/clipboard', () => jest.fn());
jest.mock('@iconify-icons/carbon/document-pdf', () => jest.fn());
jest.mock('@iconify-icons/typcn/document-text', () => jest.fn());
jest.mock('@iconify-icons/akar-icons/folder', () => jest.fn());
jest.mock('@iconify/icons-carbon/group-presentation', () => jest.fn());
jest.mock('@iconify-icons/akar-icons/image', () => jest.fn());
jest.mock('@iconify-icons/bi/info-circle', () => jest.fn());
jest.mock('@iconify/icons-feather/link', () => jest.fn());
jest.mock('@iconify/icons-feather/link-2', () => jest.fn());
jest.mock('@iconify-icons/akar-icons/link-out', () => jest.fn());
jest.mock('@iconify-icons/fe/mail', () => jest.fn());
jest.mock('@iconify-icons/mdi/microsoft-excel', () => jest.fn());
jest.mock('@iconify-icons/mdi/microsoft-powerpoint', () => jest.fn());
jest.mock('@iconify-icons/mdi/microsoft-word', () => jest.fn());
jest.mock('@iconify/icons-cil/note-add', () => jest.fn());
jest.mock('@iconify/icons-carbon/object-storage', () => jest.fn());
jest.mock('@iconify/icons-feather/user', () => jest.fn());
jest.mock('@iconify/icons-feather/users', () => jest.fn());
jest.mock('@iconify-icons/feather/x-circle', () => jest.fn());