import { toValue } from "vue";

export function useReplaceIncorrectImageUrl(input_string) {
    const value = toValue(input_string);
    const reg = new RegExp(
        '/<img src="../private/[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}">'
    );

    //Using regex - we are finding the img src and removing the ../
    return value.replace(
        reg,
        (match) => {
            return match.replace("../", "/");
        }
    );
}