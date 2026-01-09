<script setup lang="ts">
import { ButtonVariantEnum } from '@/utils/enums/ButtonVariantEnum.ts';
import { ObjectStateEnum } from '@/utils/enums/ObjectStateEnum.ts';
import { computed } from 'vue';

const props = defineProps({
    label: {
        type: String,
        required: true,
    },
    objectState: {
        required: true,
        // This is broken - the value does not translate back into the object state
        validator: function (value: string): boolean {
            const enumValues: string[] = Object.values(ObjectStateEnum);
            return enumValues.includes(value);
        },
    },
    variant: {
        required: false,
        default: ButtonVariantEnum.Primary,
        validator: function (value: string): boolean {
            const enumValues: string[] = Object.values(ButtonVariantEnum);
            return enumValues.includes(value);
        },
    },
});

const buttonText = computed(() => {
    let button_text = props.label;

    switch (props.objectState) {
        case ObjectStateEnum.Loading:
            button_text = 'Loading...';
            break;
        case ObjectStateEnum.Saving:
            button_text = 'Saving...';
            break;
        case ObjectStateEnum.Error:
            button_text = 'Error!';
            break;
        default:
            break;
    }
    return button_text;
});

const classAttributes = computed(() => {
    let class_attribute = props.variant.toString();

    switch (props.objectState) {
        case ObjectStateEnum.Loading:
        case ObjectStateEnum.Saving:
            class_attribute = class_attribute + ' loading';
            break;
        case ObjectStateEnum.Disable:
            class_attribute = class_attribute + ' disable';
            break;
        case ObjectStateEnum.Error:
            class_attribute = class_attribute + ' error';
            break;
        default:
            break;
    }

    // Return the class attribute
    return class_attribute;
});

const isDisabled = computed(() => {
    return props.objectState !== ObjectStateEnum.NoAction;
});
</script>

<template>
    <button :class="classAttributes" :disabled="isDisabled">
        {{ buttonText }}
    </button>
</template>

<style scoped>
button {
    padding: 0.5rem 1rem;
    border: var(--border);
    border-radius: var(--border-radius);
    border-width: var(--border-width);
    border-style: var(--border-style);
    color: var(--text);

	&.compact {
		padding: 0.25rem 0.125rem;
		font-size: 0.75rem;
		line-height: 1rem;
	}

	&.tiny {
		padding: 0.125rem 0rem;
		font-size: 0.75rem;
		line-height: 0.75rem;
	}

    &.primary {
        background-color: var(--primary);
        border-color: var(--primary);

        &:hover {
            &:enabled {
                background-color: var(--primary-hover);
            }
        }
    }

    &.secondary {
        background-color: var(--secondary);
        border-color: var(--secondary);

        &:hover {
            &:enabled {
                background-color: var(--secondary-hover);
            }
        }
    }

    &.danger {
        background-color: var(--danger);
        border-color: var(--danger);

        &:hover {
            &:enabled {
                background-color: var(--danger-hover);
            }
        }
    }

    &.warning {
        background-color: var(--warning);
        border-color: var(--warning);

        &:hover {
            &:enabled {
                background-color: var(--warning-hover);
            }
        }
    }

    &.success {
        background-color: var(--success);
        border-color: var(--success);

        &:hover {
            &:enabled {
                background-color: var(--success-hover);
            }
        }
    }

    &.info {
        background-color: var(--info);
        border-color: var(--info);

        &:hover {
            &:enabled {
                background-color: var(--info-hover);
            }
        }
    }

    &.loading {
        animation: loading-animation 1s infinite linear;
    }
}

@keyframes loading-animation {
    0% {
        color: var(--text);
    }
    50% {
        color: var(--text-muted);
    }
    100% {
        color: var(--text);
    }
}
</style>
