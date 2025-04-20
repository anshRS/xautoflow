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
                  _buildTaskTypeChip(theme),
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

  Widget _buildTaskTypeChip(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: _getTaskTypeColor(theme).withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            _getTaskTypeIcon(),
            size: 16,
            color: _getTaskTypeColor(theme),
          ),
          const SizedBox(width: 4),
          Text(
            task.type.name,
            style: theme.textTheme.bodySmall?.copyWith(
              color: _getTaskTypeColor(theme),
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusChip(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: _getStatusColor(theme).withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        task.status.name,
        style: theme.textTheme.bodySmall?.copyWith(
          color: _getStatusColor(theme),
          fontWeight: FontWeight.w500,
        ),
      ),
    );
  }

  Color _getTaskTypeColor(ThemeData theme) {
    switch (task.type) {
      case TaskType.research:
        return theme.colorScheme.primary;
      case TaskType.strategy:
        return theme.colorScheme.secondary;
      case TaskType.backtest:
        return theme.colorScheme.tertiary;
      default:
        return theme.colorScheme.primary;
    }
  }

  IconData _getTaskTypeIcon() {
    switch (task.type) {
      case TaskType.research:
        return Icons.search;
      case TaskType.strategy:
        return Icons.analytics;
      case TaskType.backtest:
        return Icons.history;
      default:
        return Icons.task;
    }
  }

  Color _getStatusColor(ThemeData theme) {
    switch (task.status) {
      case TaskStatus.pending:
        return theme.colorScheme.primary;
      case TaskStatus.inProgress:
        return theme.colorScheme.secondary;
      case TaskStatus.completed:
        return theme.colorScheme.tertiary;
      case TaskStatus.failed:
        return theme.colorScheme.error;
      default:
        return theme.colorScheme.primary;
    }
  }
} 