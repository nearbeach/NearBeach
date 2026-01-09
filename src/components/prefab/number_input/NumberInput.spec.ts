import { describe, expect, test } from "vitest";
import { render } from "vitest-browser-vue";
import { mount } from "@vue/test-utils";
import NumberInput from "./NumberInput.vue";

// LABEL
describe("NumberInput - Label testing", async () => {
  test('renders label when input exists - "hello world"', async () => {
    const { getByText } = render(NumberInput, {
      props: {
        label: "hello world",
      },
    });

    // Label is being rendered correctly
    await expect.element(getByText("hello world")).toBeInTheDocument();
  });

  test('renders label when input exists - "Number Picker"', async () => {
    const { getByText } = render(NumberInput, {
      props: {
        label: "Number Picker",
      },
    });

    // Label is being rendered correctly
    await expect.element(getByText("Number Picker")).toBeInTheDocument();
  });
});

// INCREMENTING ++
describe("NumberInput - Incrementing", async () => {
  test("counters increase from 0 to 1 when increase is clicked", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has been increased by 1
    expect(wrapper.find("input").element.value).toBe("1");
  });

  test("increment to the max value and check button gets disabled", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
        modelValue: 9,
      },
    });

    // Assert input value is default 10
    expect(wrapper.find("input").element.value).toBe("9");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Expect to be disabled
    expect(targetButton?.element.disabled).toBe(false);

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has changed, and button is disabled
    expect(wrapper.find("input").element.value).toBe("10");
    expect(targetButton?.element.disabled).toBe(true);
  });

  test("increment button is disabled and will not increment the value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
        modelValue: 10,
      },
    });

    // Assert input value is default 9
    expect(wrapper.find("input").element.value).toBe("10");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Expect to be disabled
    expect(targetButton?.element.disabled).toBe(true);

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("10");
  });

  test("increment by 5 units", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
        modelValue: 0,
        stepIncrement: 5,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value added 5 units
    expect(wrapper.find("input").element.value).toBe("5");
  });

  test("increment past the maxValue, results should return max value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
        modelValue: 0,
        stepIncrement: 15,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("10");
  });

  test("increment by 1 to the max javascript integer value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: Number.MAX_SAFE_INTEGER,
        modelValue: Number.MAX_SAFE_INTEGER - 1,
        stepIncrement: 1,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe(
      `${Number.MAX_SAFE_INTEGER - 1}`,
    );

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe(
      `${Number.MAX_SAFE_INTEGER}`,
    );
  });

  test("increment by 10 PAST the max javascript integer value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: Number.MAX_SAFE_INTEGER,
        modelValue: Number.MAX_SAFE_INTEGER - 1,
        stepIncrement: 10,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe(
      `${Number.MAX_SAFE_INTEGER - 1}`,
    );

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe(
      `${Number.MAX_SAFE_INTEGER}`,
    );
  });

  test("counters increase from 0 to 1 when increase is clicked, even with a -1 step increment", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: 0,
        stepIncrement: -1,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("1");
  });

  test("counters increase from -10 to -9 when increase is clicked", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: -10,
      },
    });

    // Assert input value is default
    expect(wrapper.find("input").element.value).toBe("-10");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-9");
  });

  test("counters increase from -12 to -10 when increase is clicked, even with a -2 step increment", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: -12,
        stepIncrement: -2,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("-12");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-10");
  });

  test("we can still increment even when the model value is less than the minimum value. Will instantly pop to minimum number", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
        modelValue: -15,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("-15");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("+"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-10");
  });
});

// DECREMENTING ++
describe("NumberInput - Decreasing", async () => {
  test("counters decreases from 0 to -1 when decrease is clicked", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has been increased by 1
    expect(wrapper.find("input").element.value).toBe("-1");
  });

  test("decrease to the min value and check button gets disabled", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
        modelValue: -9,
      },
    });

    // Assert input value is default
    expect(wrapper.find("input").element.value).toBe("-9");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Expect to be disabled
    expect(targetButton?.element.disabled).toBe(false);

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has changed, and button is disabled
    expect(wrapper.find("input").element.value).toBe("-10");
    expect(targetButton?.element.disabled).toBe(true);
  });

  test("decrement button is disabled and will not decrease the value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
        modelValue: -10,
      },
    });

    // Assert input value is default
    expect(wrapper.find("input").element.value).toBe("-10");

    // Find the + button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Expect to be disabled
    expect(targetButton?.element.disabled).toBe(true);

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-10");
  });

  test("decrement by 5 units", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
        modelValue: 0,
        stepIncrement: 5,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value added 5 units
    expect(wrapper.find("input").element.value).toBe("-5");
  });

  test("decrement past the minValue, results should return min value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
        modelValue: 0,
        stepIncrement: 15,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-10");
  });

  test("decrement by 1 to the min javascript integer value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -Number.MAX_SAFE_INTEGER,
        modelValue: -Number.MAX_SAFE_INTEGER + 1,
        stepIncrement: 1,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe(
      `${-Number.MAX_SAFE_INTEGER + 1}`,
    );

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe(
      `${-Number.MAX_SAFE_INTEGER}`,
    );
  });

  test("decrement by 10 PAST the min javascript integer value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -Number.MAX_SAFE_INTEGER,
        modelValue: -Number.MAX_SAFE_INTEGER + 1,
        stepIncrement: 10,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe(
      `${-Number.MAX_SAFE_INTEGER + 1}`,
    );

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe(
      `${-Number.MAX_SAFE_INTEGER}`,
    );
  });

  test("counters decreases from 0 to -1 when decrease is clicked, even with a -1 step increment", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: 0,
        stepIncrement: -1,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("0");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the + button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("-1");
  });

  test("counters decrease from 10 to 9 when decrease is clicked", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: 10,
      },
    });

    // Assert input value is default
    expect(wrapper.find("input").element.value).toBe("10");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("9");
  });

  test("counters decreases from 12 to 10 when decrease is clicked, even with a -2 step increment", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: 12,
        stepIncrement: -2,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("12");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("10");
  });

  test("we can still decrement even when the model value is more than the maximum value. Will instantly pop to maximum number", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
        modelValue: 15,
      },
    });

    // Assert input value is default 0
    expect(wrapper.find("input").element.value).toBe("15");

    // Find the - button
    const buttons = wrapper.findAll("button");
    const targetButton = buttons.filter((buttonWrapper) =>
      buttonWrapper.text().includes("-"),
    )[0];

    // Click on the - button
    await targetButton?.trigger("click");

    // Check the value has not changed
    expect(wrapper.find("input").element.value).toBe("10");
  });
});

describe("NumberInput - Manually Entering", async () => {
  test("manually enter in the value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
      },
    });

    // Check the default value
    const input = wrapper.find("input");
    expect(input.element.value).toBe("0");

    // Mutate to 15
    await input.setValue("15");

    // Check the value
    expect(input.element.value).toBe("15");
  });

  test("manually enter the value past the max value, should update to max value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        maxValue: 10,
      },
    });

    // Check the default value
    const input = wrapper.find("input");
    expect(input.element.value).toBe("0");

    // Mutate to 15
    await input.setValue("15");

    // Check the value
    expect(input.element.value).toBe("10");
  });

  test("manually enter the value under the min value, should update to min value", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        minValue: -10,
      },
    });

    // Check the default value
    const input = wrapper.find("input");
    expect(input.element.value).toBe("0");

    // Mutate to 15
    await input.setValue("-15");

    // Check the value
    expect(input.element.value).toBe("-10");
  });

  test("manually remove all values - should default to 0", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
        modelValue: 100,
      },
    });

    // Check the default value
    const input = wrapper.find("input");
    expect(input.element.value).toBe("100");

    // Mutate to ""
    await input.setValue("");

    // Check the value
    expect(input.element.value).toBe("0");
  });

  test("manual - user tries to type in -1. First they hit -, default will be -1", async () => {
    const wrapper = mount(NumberInput, {
      props: {
        label: "Test Number",
      },
    });

    // Check the default value
    const input = wrapper.find("input");
    expect(input.element.value).toBe("0");

    // Mutate to ""
    await input.setValue("-");

    // Check the value
    expect(input.element.value).toBe("0");
  });
});
