import { toValue } from "vue";

export function useToken(tokenName) {
    const value = toValue(tokenName);

    //Use regex to extract out the require token
    const regEx = new RegExp(`${value}=([^;]+)`);
    const valueArray = regEx.exec(document.cookie);
    return valueArray !== null ? encodeURIComponent(valueArray[1]) : null;
}