import type {DocumentItemInterface} from "@/utils/interfaces/documents/DocumentItemInterface.ts";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";

export interface FileSystemInterface {
    documents: DocumentItemInterface[],
    folders: FolderItemInterface[],
    max_upload_size: number,
}