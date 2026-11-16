export interface AuditChangeInterface {
  old: unknown,
  new: unknown,
}

export interface AuditLogItemInterface {
  id: number,
  date_created: string,
  username: string,
  action: string,
  summary: string,
  changes: Record<string, AuditChangeInterface>,
}

export interface AuditLogPageInterface {
  count: number,
  next: string | null,
  previous: string | null,
  results: AuditLogItemInterface[],
}
