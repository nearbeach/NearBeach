export interface DocumentItemInterface {
    description: string;
    document: string | null;
    folder: string | null;
    key: string;
    parent_folder_id: number | null,
    url_location: string | null;
}