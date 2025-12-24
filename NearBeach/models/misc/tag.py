class Tag(models.Model):
    tag_id = models.BigAutoField(primary_key=True)
    tag_name = models.CharField(
        max_length=50,
    )
    tag_colour = models.CharField(
        max_length=7,
        default="#651794",
    )
    tag_text_colour = models.CharField(
        max_length=7,
        default="#ffffff",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.tag_name)


class TagAssignment(models.Model):
    class ObjectEnum(models.TextChoices):
        REQUIREMENT = "requirement", _("Requirement")
        REQUIREMENT_ITEM = "requirement_item", _("Requirement Item")
        PROJECT = "project", _("Project")
        TASK = "task", _("Task")
        KANBAN = "kanban_board", _("Kanban Board")
        CARD = "kanban_card", _("Kanban Card")
        REQUEST_FOR_CHANGE = "request_for_change", _("Request for Change")
        CUSTOMER = "customer", _("Customer")
        ORGANISATION = "organisation", _("Organisation")

    tag_assignment_id = models.BigAutoField(primary_key=True)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )
    object_enum = models.CharField(
        max_length=40,
        choices=ObjectEnum.choices,
        default=ObjectEnum.REQUIREMENT,
    )
    object_id = models.IntegerField(
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s_change_user"
    )
    is_deleted = models.BooleanField(
        default=False,
    )
