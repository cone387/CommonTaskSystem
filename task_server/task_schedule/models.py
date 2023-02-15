from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from .choices import TaskStatus, TaskScheduleStatus, TaskScheduleType, TaskCallbackStatus
from common_objects.models import CommonTag, CommonCategory
from common_objects import fields as common_fields


UserModel = get_user_model()


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey('self', db_constraint=False, on_delete=models.DO_NOTHING,
                               null=True, blank=True, verbose_name='父任务')
    name = models.CharField(max_length=100, verbose_name='任务名')
    category = models.ForeignKey(CommonCategory, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name='类别')
    tags = models.ManyToManyField(CommonTag, db_constraint=False, verbose_name='标签')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    config = common_fields.ConfigField(default=common_fields.get_default_config('Task'),
                                       blank=True, null=True, verbose_name='参数')
    status = common_fields.CharField(max_length=1, default=TaskStatus.ENABLE.value, verbose_name='状态',
                                     choices=TaskStatus.choices)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_constraint=False, verbose_name='用户')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'taskhub'
        verbose_name = verbose_name_plural = '任务中心'
        unique_together = ('name', 'user', 'parent')

    def __str__(self):
        return self.name

    __repr__ = __str__


class TaskCallback(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='回调')
    status = common_fields.CharField(default=TaskCallbackStatus.ENABLE.value, verbose_name='状态',
                                     choices=TaskCallbackStatus.choices)
    config = common_fields.ConfigField(default=common_fields.get_default_config('TaskCallback'), blank=True, null=True,
                                       verbose_name='参数')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_constraint=False, verbose_name='用户')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'task_callback'
        verbose_name = verbose_name_plural = '任务回调'
        unique_together = ('name', 'user')

    def __str__(self):
        return self.name

    __repr__ = __str__


class TaskSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_constraint=False, verbose_name='任务')
    type = common_fields.CharField(default=TaskScheduleType.CONTINUOUS.value, verbose_name='计划类型',
                                   choices=TaskScheduleType.choices)
    crontab = models.CharField(max_length=50, null=True, blank=True, verbose_name='Crontab表达式')
    priority = models.IntegerField(default=0, verbose_name='优先级')
    next_schedule_time = models.DateTimeField(default=timezone.now, verbose_name='下次运行时间')
    period = models.IntegerField(default=60, verbose_name='周期(秒)')
    status = common_fields.CharField(default=TaskScheduleStatus.OPENING.value, verbose_name='状态',
                                     choices=TaskScheduleStatus.choices)
    callback = models.ForeignKey(TaskCallback, on_delete=models.CASCADE,
                                 null=True, blank=True, db_constraint=False, verbose_name='回调')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_constraint=False, verbose_name='用户')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'task_schedule'
        verbose_name = verbose_name_plural = '任务计划'

    def __str__(self):
        return self.task.name

    __repr__ = __str__


class TaskScheduleLog(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(TaskSchedule, db_constraint=False, on_delete=models.CASCADE, verbose_name='任务计划')
    status = common_fields.CharField(verbose_name='运行状态')
    result = common_fields.ConfigField(blank=True, null=True, verbose_name='结果')
    schedule_time = models.DateTimeField(verbose_name='计划时间')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')

    @property
    def finish_time(self):
        return self.create_time

    class Meta:
        db_table = 'task_schedule_log'
        verbose_name = verbose_name_plural = '任务日志'

    def __str__(self):
        return "schedule: %s, status: %s" % (self.schedule, self.status)

    __repr__ = __str__