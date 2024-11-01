import { toValue } from "vue";

export function useDisableDate(timeStamp) {
    const value = toValue(timeStamp);

    //Get date but level the time to 00:00:00
    const date = new Date();
    date.setMilliseconds(0);
    date.setSeconds(0);
    date.setMinutes(0);
    date.setHours(0);

    //Return anything that is less than a day ago.
    return value <= date.getTime() - 3600000;
}
