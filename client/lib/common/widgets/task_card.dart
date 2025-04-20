import 'package:flutter/material.dart';
import 'package:client/core/models/task.dart';
import 'package:client/core/theme/app_theme.dart';
import 'package:timeago/timeago.dart' as timeago;

class TaskCard extends StatelessWidget {
  final Task task;
  final VoidCallback onTap;

  const TaskCard({
    Key? key,
    required this.task,
    required this.onTap,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  _buildTaskTypeChip(),
                  const Spacer(),
                  _buildStatusChip(theme),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                task.title,
                style: theme.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              if (task.description != null) ...[
                const SizedBox(height: 8),
                Text(
                  task.description!,
                  style: theme.textTheme.bodyMedium,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
              const SizedBox(height: 16),
              Row(
                children: [
                  Icon(
                    Icons.access_time,
                    size: 16,
                    color: theme.textTheme.bodySmall?.color,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    timeago.format(task.createdAt),
                    style: theme.textTheme.bodySmall,
                  ),
                  const Spacer(),
                  if (task.dueDate != null) ...[
                    Icon(
                      Icons.calendar_today,
                      size: 16,
                      color: theme.textTheme.bodySmall?.color,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      timeago.format(task.dueDate!),
                      style: theme.textTheme.bodySmall,
                    ),
                  ],
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTaskTypeChip() {
    return Chip(
      label: Text(_getTaskTypeName(task.taskType)),
      backgroundColor: _getTaskTypeColor(),
      labelStyle: const TextStyle(fontSize: 12),
    );
  }

  String _getTaskTypeName(TaskType type) {
    switch (type) {
      case TaskType.research:
        return 'Research';
      case TaskType.strategyDev:
        return 'Strategy Dev';
      case TaskType.backtest:
        return 'Backtest';
    }
  }

  Color _getTaskTypeColor() {
    switch (task.taskType) {
      case TaskType.research:
        return Colors.blue.shade100;
      case TaskType.strategyDev:
        return Colors.green.shade100;
      case TaskType.backtest:
        return Colors.orange.shade100;
    }
  }

  Color _getTaskTypeIconColor() {
    switch (task.taskType) {
      case TaskType.research:
        return Colors.blue;
      case TaskType.strategyDev:
        return Colors.green;
      case TaskType.backtest:
        return Colors.orange;
    }
  }

  IconData _getTaskTypeIcon() {
    switch (task.taskType) {
      case TaskType.research:
        return Icons.search;
      case TaskType.strategyDev:
        return Icons.trending_up;
      case TaskType.backtest:
        return Icons.history;
    }
  }

  Widget _buildStatusChip(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: _getStatusColor(theme).withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            _getStatusIcon(),
            size: 16,
            color: _getStatusColor(theme),
          ),
          const SizedBox(width: 4),
          Text(
            task.status.name,
            style: theme.textTheme.bodySmall?.copyWith(
              color: _getStatusColor(theme),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Color _getStatusColor(ThemeData theme) {
    switch (task.status) {
      case TaskStatus.planning:
        return Colors.grey;
      case TaskStatus.pendingApproval:
        return Colors.orange;
      case TaskStatus.running:
        return Colors.blue;
      case TaskStatus.completed:
        return Colors.green;
      case TaskStatus.failed:
        return Colors.red;
    }
  }

  IconData _getStatusIcon() {
    switch (task.status) {
      case TaskStatus.planning:
        return Icons.edit;
      case TaskStatus.pendingApproval:
        return Icons.pending;
      case TaskStatus.running:
        return Icons.play_arrow;
      case TaskStatus.completed:
        return Icons.check;
      case TaskStatus.failed:
        return Icons.error;
    }
  }
} 