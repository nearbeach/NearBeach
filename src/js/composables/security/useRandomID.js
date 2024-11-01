export function useRandomID() {
    //If crypto.randomUUID works on browser - use that by default
    if (crypto.randomUUID !== undefined) return crypto.randomUUID();

    //Cryptop Random UUID did not work - default is to manually create uuid
    let results = "";
    const characters = "abcdefghijklmnopqrstuvwxyz0123456789";

    //Loop through to create random 6 string
    for (let i = 0; i < 6; i++) {
        results += characters.charAt(
            Math.floor(Math.random() * characters.length)
        );
    }

    //Return our random string
    return results;
}