import 'package:json_annotation/json_annotation.dart';
import 'package:uuid/uuid.dart';

part 'task.g.dart';

enum TaskType {
  @JsonValue('RESEARCH')
  research,
  @JsonValue('STRATEGY_DEV')
  strategyDev,
  @JsonValue('BACKTEST')
  backtest,
}

enum TaskStatus {
  @JsonValue('PLANNING')
  planning,
  @JsonValue('PENDING_APPROVAL')
  pendingApproval,
  @JsonValue('RUNNING')
  running,
  @JsonValue('COMPLETED')
  completed,
  @JsonValue('FAILED')
  failed,
}

@JsonSerializable()
class Task {
  final String id;
  final String title;
  final String? description;
  final TaskType taskType;
  final TaskStatus status;
  final Map<String, dynamic> inputData;
  final Map<String, dynamic>? generatedPlan;
  final Map<String, dynamic>? result;
  final String? errorDetails;
  final DateTime createdAt;
  final DateTime updatedAt;
  final DateTime? dueDate;

  Task({
    required this.id,
    required this.title,
    this.description,
    required this.taskType,
    required this.status,
    required this.inputData,
    this.generatedPlan,
    this.result,
    this.errorDetails,
    required this.createdAt,
    required this.updatedAt,
    this.dueDate,
  });

  factory Task.fromJson(Map<String, dynamic> json) => _$TaskFromJson(json);
  Map<String, dynamic> toJson() => _$TaskToJson(this);

  Task copyWith({
    String? id,
    String? title,
    String? description,
    TaskType? taskType,
    TaskStatus? status,
    Map<String, dynamic>? inputData,
    Map<String, dynamic>? generatedPlan,
    Map<String, dynamic>? result,
    String? errorDetails,
    DateTime? createdAt,
    DateTime? updatedAt,
    DateTime? dueDate,
  }) {
    return Task(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      taskType: taskType ?? this.taskType,
      status: status ?? this.status,
      inputData: inputData ?? this.inputData,
      generatedPlan: generatedPlan ?? this.generatedPlan,
      result: result ?? this.result,
      errorDetails: errorDetails ?? this.errorDetails,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      dueDate: dueDate ?? this.dueDate,
    );
  }
}

@JsonSerializable()
class TaskCreate {
  final String title;
  final String? description;
  final TaskType taskType;
  final Map<String, dynamic> inputData;
  final DateTime? dueDate;

  TaskCreate({
    required this.title,
    this.description,
    required this.taskType,
    required this.inputData,
    this.dueDate,
  });

  factory TaskCreate.fromJson(Map<String, dynamic> json) => _$TaskCreateFromJson(json);
  Map<String, dynamic> toJson() => _$TaskCreateToJson(this);
}

@JsonSerializable()
class PlanApproval {
  final bool approved;
  final Map<String, dynamic>? modifiedPlan;

  PlanApproval({
    required this.approved,
    this.modifiedPlan,
  });

  factory PlanApproval.fromJson(Map<String, dynamic> json) => _$PlanApprovalFromJson(json);
  Map<String, dynamic> toJson() => _$PlanApprovalToJson(this);
} 