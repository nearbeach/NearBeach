import type {ObjectStatusInterface} from "@/utils/interfaces/stores/ObjectStatusInterface.ts";
import type {ObjectTypesInterface} from "@/utils/interfaces/stores/ObjectTypesInterface.ts";
import type {TagsInterface} from "@/utils/interfaces/stores/TagsInterface.ts";
import type {StatusInterface} from "@/utils/interfaces/stores/StatusInterface.ts";
import type {TypesInterface} from "@/utils/interfaces/stores/TypesInterface.ts";


export interface ObjectMetaDataInterface {
    isLoaded: boolean,
    object_status: ObjectStatusInterface[],
    object_types: ObjectTypesInterface[],
    tags: TagsInterface[],
    status: StatusInterface[],
    type: TypesInterface[],
}