class ObjectNote(models.Model):
    object_note_id = models.BigAutoField(primary_key=True)
    object_note = models.TextField(
        blank=False,
        default="",
    )
    kanban_card = models.ForeignKey(
        "KanbanCard",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        "RequestForChange",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )
