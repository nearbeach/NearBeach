<script setup lang="ts">
import CardHeader from '@/components/prefab/card/card_header/CardHeader.vue';
import CardComponent from '@/components/prefab/card/CardComponent.vue';
</script>

<template>
    <CardComponent class="dashboard-page">
        <CardHeader>
            <h1 id="main-title">Welcome to the Redesign</h1>
            <p class="sub-text">We are looking for you feedback</p>
        </CardHeader>

        <h2 style="margin-top: -1rem">Why have we built this?</h2>
        <p>
            The community of users are very imported to NearBeach and it's
            development. Over the past number of years NearBeach has had many
            great contributions from it's Users and the community. This
            includes; code, feature requests, and bug reports.
        </p>
        <p>We are currently looking for feedback on NearBeach's new design.</p>

        <h2>Why the vertical slice?</h2>
        <p>
            We would love to get the design into your hands a lot quicker, so
            we've had to cut down how much we are including within the vertical
            slice. This means we'll have less to develop and fix as we get
            feedback. Thus speeding up the feedback loop.
        </p>
        <p>We have only implemented the following sections;</p>
        <ul>
            <li>
                Project Search -
                <span style="font-weight: lighter"
                    >Click on the "Project" item in the Navbar</span
                >
            </li>
            <li>
                New Project -
                <span style="font-weight: lighter"
                    >Click on the + on the "Project" item in the Navbar</span
                >
            </li>
            <li>
                Project Information -
                <span style="font-weight: lighter">To be constructed</span>
            </li>
        </ul>

        <h2>Where can I give feedback?</h2>
        <p>All feedback can be given to us on either;</p>
        <ul>
            <li>
                <a
                    href="https://discord.gg/64uhRztS6n"
                    ref="no-follow no-index"
                    target="_blank"
                    >Discord</a
                >
            </li>
            <li>
                <a
                    href="https://x.com/robotichead"
                    ref="no-follow no-index"
                    target="_blank"
                    >Twitter</a
                >
            </li>
            <li>
                <a
                    href="https://bsky.app/profile/robotichead.bsky.social"
                    ref="no-follow no-index"
                    target="_blank"
                    >Bluesky</a
                >
            </li>
        </ul>
    </CardComponent>
</template>

<style scoped>
.dashboard-page {
    display: grid;
    grid-template-columns: 1fr;
    max-width: var(--large-grid-width);
    margin: auto;
    padding: 0 0.5rem;

    @media (--small-screen) {
        padding: 0.5rem 1rem;
    }

    @media (--large-screen) {
        padding: 1rem 2rem;
    }
}
</style>
