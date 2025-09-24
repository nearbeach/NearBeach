# Contributing to NearBeach

If you would like to join our community, please join our [fun and exciting discord](https://discord.gg/64uhRztS6n).

## Contributing to NearBeach

We are always looking for new contributors. There are many different ways to contribute to NearBeach, for example;

-   Donating via [github sponsorships](https://github.com/sponsors/NearBeach) or [our patreon](https://www.patreon.com/NearBeach)
-   Bug testing
-   Bug fixing
-   Writing Documentation
-   Writing new components or functionality for NearBeach
-   Refactoring Code, i.e. making it more efficient
-   Updating Code, i.e. updating libraries
-   Marketing NearBeach
-   Supplying feedback on NearBeach, i.e. improvements and feature requests

and many many more. Join our [community on discord to see what you can do](https://discord.gg/64uhRztS6n)

## Code of Conduct

Please read our [code of conduct here](https://github.com/NearBeach/NearBeach/blob/main/CODE_OF_CONDUCT.md).

## NearBeach Overview

NearBeach is an open source project management system, that has been built using both the frameworks; Django and VueJS.

### Objects in NearBeach

Each different module/componet in NearBeach are called Objects. The following objects currently exist;

-   Organisations
-   Customers
-   Requirements
-   Requirement Items
-   Projects
-   Tasks
-   Request for Changes
-   Kanban Boards

Each object shall have it's own folder structure within the respected location, i.e. `/views/projects`.

## Setting up local dev environment

Please follow the instructions in our documentation: [Setting up local dev environment](https://nearbeach.readthedocs.io/en/latest/002-local-development-environment-setup/index.html)

## Coding Style Guides

These style guides at the moment, are a recommendation. However are not followed strickly at the moment. We are looking at implementing automatic linting in the near future.

### Vue 3

Please refer to the [Vue 3 Style Guides located on their documentation](https://vuejs.org/style-guide/)

Please note the following outliers

- Local variables within a function are usually done in snake_case to differentiate them from the object and prop variables

EXAMPLE CODE

    <template>
    ...
    </template>
    <script>
        export default {
            name: "ExampleComponent",
            props: {
                propVariable: {
                    type: String,
                    default: "value",
                }
                ...
            },
            data() {
                return {
                    dataVariable: "value",
                    ...
                }
            },
            methods: {
                myMethod(input_variable) {
                    // Notice the "input_variable" is in snake case.
                    ...
                },
            },
        }
    </script>

### Python

Please refer to the [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)

## Donating

Like most projects, there are some overhead costs. Every single dollar that we get will go towards;

-   Software costs
-   Administration costs
-   Freelance costs (i.e. hiring help like designers)

We are being transparent with all our costs and will try and provide a yearly cost breakdown every 6 months.

## Bug Reporting

Bug reporting is a very important role for NearBeach. During Hacktoberfest, you are more than welcome to submit issues.

## Pull Requests

Please fork NearBeach, git your changes in and then submit a simple pull request.

When submitting a pull request, please fill out the template appropriately. We have flagged NearBeach's repository with Hacktoberfest, so any accepted pull requests WILL count towards Hacktoberfest.

Not all pull requests will be accepted.

## Documentation

Our documentation is hosted on [readthedocs](https://nearbeach.readthedocs.io). If you would like to contribute to the documentation, you will be able to find the files within `/docs`
