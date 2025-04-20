// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'task.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

Task _$TaskFromJson(Map<String, dynamic> json) => Task(
  id: json['id'] as String,
  title: json['title'] as String,
  description: json['description'] as String?,
  taskType: $enumDecode(_$TaskTypeEnumMap, json['taskType']),
  status: $enumDecode(_$TaskStatusEnumMap, json['status']),
  inputData: json['inputData'] as Map<String, dynamic>,
  generatedPlan: json['generatedPlan'] as Map<String, dynamic>?,
  result: json['result'] as Map<String, dynamic>?,
  errorDetails: json['errorDetails'] as String?,
  createdAt: DateTime.parse(json['createdAt'] as String),
  updatedAt: DateTime.parse(json['updatedAt'] as String),
  dueDate:
      json['dueDate'] == null
          ? null
          : DateTime.parse(json['dueDate'] as String),
);

Map<String, dynamic> _$TaskToJson(Task instance) => <String, dynamic>{
  'id': instance.id,
  'title': instance.title,
  'description': instance.description,
  'taskType': _$TaskTypeEnumMap[instance.taskType]!,
  'status': _$TaskStatusEnumMap[instance.status]!,
  'inputData': instance.inputData,
  'generatedPlan': instance.generatedPlan,
  'result': instance.result,
  'errorDetails': instance.errorDetails,
  'createdAt': instance.createdAt.toIso8601String(),
  'updatedAt': instance.updatedAt.toIso8601String(),
  'dueDate': instance.dueDate?.toIso8601String(),
};

const _$TaskTypeEnumMap = {
  TaskType.research: 'RESEARCH',
  TaskType.strategyDev: 'STRATEGY_DEV',
  TaskType.backtest: 'BACKTEST',
};

const _$TaskStatusEnumMap = {
  TaskStatus.planning: 'PLANNING',
  TaskStatus.pendingApproval: 'PENDING_APPROVAL',
  TaskStatus.running: 'RUNNING',
  TaskStatus.completed: 'COMPLETED',
  TaskStatus.failed: 'FAILED',
};

TaskCreate _$TaskCreateFromJson(Map<String, dynamic> json) => TaskCreate(
  title: json['title'] as String,
  description: json['description'] as String?,
  taskType: $enumDecode(_$TaskTypeEnumMap, json['taskType']),
  inputData: json['inputData'] as Map<String, dynamic>,
  dueDate:
      json['dueDate'] == null
          ? null
          : DateTime.parse(json['dueDate'] as String),
);

Map<String, dynamic> _$TaskCreateToJson(TaskCreate instance) =>
    <String, dynamic>{
      'title': instance.title,
      'description': instance.description,
      'taskType': _$TaskTypeEnumMap[instance.taskType]!,
      'inputData': instance.inputData,
      'dueDate': instance.dueDate?.toIso8601String(),
    };

PlanApproval _$PlanApprovalFromJson(Map<String, dynamic> json) => PlanApproval(
  approved: json['approved'] as bool,
  modifiedPlan: json['modifiedPlan'] as Map<String, dynamic>?,
);

Map<String, dynamic> _$PlanApprovalToJson(PlanApproval instance) =>
    <String, dynamic>{
      'approved': instance.approved,
      'modifiedPlan': instance.modifiedPlan,
    };
