import 'package:flutter/material.dart';
import 'package:timeago/timeago.dart' as timeago;
import 'package:client/core/models/task.dart';

class TaskDetailsScreen extends StatelessWidget {
  final Task task;

  const TaskDetailsScreen({Key? key, required this.task}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Details'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      task.title,
                      style: Theme.of(context).textTheme.headlineMedium,
                    ),
                    const SizedBox(height: 8),
                    if (task.description != null) ...[
                      Text(
                        task.description!,
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                      const SizedBox(height: 16),
                    ],
                    Row(
                      children: [
                        Chip(
                          label: Text(task.taskType.name),
                          backgroundColor: _getTaskTypeColor(task.taskType),
                        ),
                        const SizedBox(width: 8),
                        Chip(
                          label: Text(task.status.name),
                          backgroundColor: _getStatusColor(task.status),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Timeline',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 8),
                    ListTile(
                      leading: const Icon(Icons.calendar_today),
                      title: const Text('Created'),
                      subtitle: Text(timeago.format(task.createdAt)),
                    ),
                    if (task.dueDate != null)
                      ListTile(
                        leading: const Icon(Icons.event),
                        title: const Text('Due Date'),
                        subtitle: Text(timeago.format(task.dueDate!)),
                      ),
                    ListTile(
                      leading: const Icon(Icons.update),
                      title: const Text('Last Updated'),
                      subtitle: Text(timeago.format(task.updatedAt)),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            if (task.generatedPlan != null) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Generated Plan',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const SizedBox(height: 8),
                      Text(task.generatedPlan.toString()),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
            if (task.result != null) ...[
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Result',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      const SizedBox(height: 8),
                      Text(task.result.toString()),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
            ],
            if (task.errorDetails != null) ...[
              Card(
                color: Colors.red.shade50,
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Error Details',
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                              color: Colors.red,
                            ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        task.errorDetails!,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Color _getTaskTypeColor(TaskType type) {
    switch (type) {
      case TaskType.research:
        return Colors.blue.shade100;
      case TaskType.strategyDev:
        return Colors.green.shade100;
      case TaskType.backtest:
        return Colors.orange.shade100;
    }
  }

  Color _getStatusColor(TaskStatus status) {
    switch (status) {
      case TaskStatus.planning:
        return Colors.grey.shade100;
      case TaskStatus.pendingApproval:
        return Colors.orange.shade100;
      case TaskStatus.running:
        return Colors.blue.shade100;
      case TaskStatus.completed:
        return Colors.green.shade100;
      case TaskStatus.failed:
        return Colors.red.shade100;
    }
  }
} 