export function getSetOfPages(destination_page, number_of_pages) {
    if (number_of_pages === 0) {
        // There is nothing to render
        return [];
    }

    if (number_of_pages <= 7) {
        // There are not enough blocks to add in the first/previous/next/last buttons
        // Array.from({length: 10}, (_, i) => i + 1)
        return Array.from(
            {length: number_of_pages},
            (_, index) => {
                return {
                    destinationPage: index + 1,
                    text: `${index + 1}`,
                }
            }
        )
    }

    if (destination_page <= 4) {
        // At the start of the pagination
        return [
            {destinationPage: 1, text: "1"},
            {destinationPage: 2, text: "2"},
            {destinationPage: 3, text: "3"},
            {destinationPage: 4, text: "4"},
            {destinationPage: 5, text: "5"},
            {destinationPage: 6, text: ">"},
            {destinationPage: number_of_pages, text: ">>"},
        ]
    }

    if (destination_page > number_of_pages - 4) {
        // At the end of the pagination
        return [
            {destinationPage: 1, text: "<<"},
            {destinationPage: number_of_pages - 5, text: "<"},
            {destinationPage: number_of_pages - 4, text: `${number_of_pages - 4}`},
            {destinationPage: number_of_pages - 3, text: `${number_of_pages - 3}`},
            {destinationPage: number_of_pages - 2, text: `${number_of_pages - 2}`},
            {destinationPage: number_of_pages - 1, text: `${number_of_pages - 1}`},
            {destinationPage: number_of_pages, text: `${number_of_pages}`},
        ]
    }

    return [
        {destinationPage: 1, text: "<<"},
        {destinationPage: destination_page - 2, text: "<"},
        {destinationPage: destination_page - 1, text: `${destination_page - 1}`},
        {destinationPage: destination_page, text: `${destination_page}`},
        {destinationPage: destination_page + 1, text: `${destination_page + 1}`},
        {destinationPage: destination_page + 2, text: ">"},
        {destinationPage: number_of_pages, text: ">>"},
    ]
}