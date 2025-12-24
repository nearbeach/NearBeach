class Sprint(models.Model):
    sprint_id = models.BigAutoField(primary_key=True)
    sprint_name = models.CharField(
        max_length=100,
        null=False,
        default="empty sprint",
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total_story_points = models.IntegerField(
        default=0,
    )
    completed_story_points = models.IntegerField(
        default=0,
    )
    sprint_status = models.CharField(
        max_length=10,
        choices=SPRINT_STATUS,
        blank=True,
        default="Draft",
    )
    sprint_start_date = models.DateTimeField()
    sprint_end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.sprint_name)

    class Meta:
        verbose_name_plural = "Sprints"
        ordering = ["-sprint_id"]


class SprintAuditTable(models.Model):
    sprint_audit_table_id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        "Sprint",
        on_delete=models.CASCADE,
    )
    story_point_cost = models.IntegerField(
        default=0,
    )
    higher_order_status = models.CharField(
        max_length=10,
        choices=OBJECT_HIGHER_ORDER_STATUS,
        default="Normal",
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )


class SprintObjectAssignment(models.Model):
    sprint_object_assignment_id = models.BigAutoField(primary_key=True)
    sprint_id = models.ForeignKey(
        "Sprint",
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        "RequirementItem",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        "Task",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )
