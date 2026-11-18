// composable/formatObjectId

export function formatObjectId(destination: string, id: number) : string {
	const objectTable = {
		customer: "cust",
		kanban_board: "kan",
		kanban_card: "card",
		request_for_change: "rfc",
		requirement: "req",
		requirement_item: "item",
		organisation: "org",
		project: "pro",
		sprint: "spr",
		task: "task",
	}

	const shortForm: string | undefined = objectTable[destination.toLowerCase() as keyof typeof objectTable];

	return `${shortForm ?? destination}-${id}`;
}