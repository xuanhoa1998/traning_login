from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
ADMIN = 'admin'
MANAGER = 'manager'
LEADER = 'leader'
MEMBER = 'member'
GUEST = 'guest'
MASTER = 'master'

USER_ROLES = (
    (MASTER, 'master'),  # 管理者
    (ADMIN, 'admin'),  # 管理者
    (MANAGER, 'manager'),  # 責任者
    (LEADER, 'leader'),  # リーダー
    (MEMBER, 'member'),  # メンバー
    (GUEST, 'guest')  # ゲスト
)


class UserRole(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='user_role_name_idx'),
            models.Index(fields=['order'], name='type_preference_order_idx'),
        ]


class User(AbstractUser):
    # Using UUID as instead of default AutoInteger ID to avoid blute force attacking.
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_service_id = models.CharField(max_length=15)
    email_signature = models.TextField(max_length=8192, blank=True, null=True)
    # Note: Remove this column after the data migration from the old system.
    old_id = models.IntegerField(null=True, unique=True, help_text='An unique ID on Old System.')
    user_role = models.ForeignKey(UserRole, on_delete=models.PROTECT, null=True)
    tel1 = models.CharField(max_length=15, blank=True, null=True)
    tel2 = models.CharField(max_length=15, blank=True, null=True)
    tel3 = models.CharField(max_length=15, blank=True, null=True)
    registed_at = models.DateTimeField(blank=True, null=True, help_text='本登録した日付')
    is_hidden = models.BooleanField(default=False, help_text='非表示ユーザフラグ')
    title = models.CharField(max_length=15, blank=True, null=True)
    age = models.IntegerField(max_length=3)