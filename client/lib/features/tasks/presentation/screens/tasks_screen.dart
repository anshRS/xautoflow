import 'package:flutter/material.dart';
import 'package:client/common/widgets/task_card.dart';
import 'package:client/core/models/task.dart';
import 'package:client/core/theme/app_theme.dart';
import 'package:client/features/tasks/presentation/screens/create_task_screen.dart';
import 'package:client/features/task_details/presentation/screens/task_details_screen.dart';
import 'package:shimmer/shimmer.dart';

class TasksScreen extends StatefulWidget {
  const TasksScreen({Key? key}) : super(key: key);

  @override
  State<TasksScreen> createState() => _TasksScreenState();
}

class _TasksScreenState extends State<TasksScreen> {
  TaskType? _selectedTaskType;
  TaskStatus? _selectedStatus;
  bool _isLoading = true;
  List<Task> _tasks = [];

  @override
  void initState() {
    super.initState();
    _loadTasks();
  }

  Future<void> _loadTasks() async {
    setState(() => _isLoading = true);
    try {
      // TODO: Replace with actual API call
      await Future.delayed(const Duration(seconds: 2));
      setState(() {
        _tasks = [];
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      // TODO: Show error message
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tasks'),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: _showFilterDialog,
          ),
        ],
      ),
      body: Column(
        children: [
          _buildFilterChips(),
          Expanded(
            child: _isLoading
                ? _buildLoadingState()
                : _tasks.isEmpty
                    ? _buildEmptyState()
                    : _buildTasksList(),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const CreateTaskScreen(),
            ),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('New Task'),
        backgroundColor: theme.colorScheme.primary,
      ),
    );
  }

  Widget _buildFilterChips() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          _buildFilterChip(
            label: 'All Types',
            isSelected: _selectedTaskType == null,
            onTap: () => setState(() => _selectedTaskType = null),
          ),
          const SizedBox(width: 8),
          ...TaskType.values.map((type) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: _buildFilterChip(
                  label: type.name,
                  isSelected: _selectedTaskType == type,
                  onTap: () => setState(() => _selectedTaskType = type),
                ),
              )),
          const SizedBox(width: 16),
          _buildFilterChip(
            label: 'All Status',
            isSelected: _selectedStatus == null,
            onTap: () => setState(() => _selectedStatus = null),
          ),
          const SizedBox(width: 8),
          ...TaskStatus.values.map((status) => Padding(
                padding: const EdgeInsets.only(right: 8),
                child: _buildFilterChip(
                  label: status.name,
                  isSelected: _selectedStatus == status,
                  onTap: () => setState(() => _selectedStatus = status),
                ),
              )),
        ],
      ),
    );
  }

  Widget _buildFilterChip({
    required String label,
    required bool isSelected,
    required VoidCallback onTap,
  }) {
    final theme = Theme.of(context);
    
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (_) => onTap(),
      backgroundColor: theme.colorScheme.surface,
      selectedColor: theme.colorScheme.primaryContainer,
      checkmarkColor: theme.colorScheme.primary,
      labelStyle: TextStyle(
        color: isSelected
            ? theme.colorScheme.onPrimaryContainer
            : theme.colorScheme.onSurface,
      ),
    );
  }

  Widget _buildLoadingState() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: 5,
      itemBuilder: (context, index) {
        return Shimmer.fromColors(
          baseColor: Colors.grey[300]!,
          highlightColor: Colors.grey[100]!,
          child: Card(
            child: Container(
              height: 120,
              margin: const EdgeInsets.only(bottom: 16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildEmptyState() {
    final theme = Theme.of(context);
    
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.task_alt,
            size: 64,
            color: theme.textTheme.bodySmall?.color,
          ),
          const SizedBox(height: 16),
          Text(
            'No tasks found',
            style: theme.textTheme.titleLarge,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),
          Text(
            'Try adjusting your filters or create a new task',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.textTheme.bodySmall?.color,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const CreateTaskScreen(),
                ),
              );
            },
            icon: const Icon(Icons.add),
            label: const Text('Create Task'),
          ),
        ],
      ),
    );
  }

  Widget _buildTasksList() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _tasks.length,
      itemBuilder: (context, index) {
        final task = _tasks[index];
        return TaskCard(
          task: task,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => TaskDetailsScreen(task: task),
              ),
            );
          },
        );
      },
    );
  }

  void _showFilterDialog() {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setState) {
            return Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Filter Tasks',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Task Type',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    children: [
                      ChoiceChip(
                        label: const Text('All'),
                        selected: _selectedTaskType == null,
                        onSelected: (selected) {
                          setState(() => _selectedTaskType = null);
                        },
                      ),
                      ...TaskType.values.map((type) => ChoiceChip(
                            label: Text(type.name),
                            selected: _selectedTaskType == type,
                            onSelected: (selected) {
                              setState(() => _selectedTaskType = type);
                            },
                          )),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Status',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 8),
                  Wrap(
                    spacing: 8,
                    children: [
                      ChoiceChip(
                        label: const Text('All'),
                        selected: _selectedStatus == null,
                        onSelected: (selected) {
                          setState(() => _selectedStatus = null);
                        },
                      ),
                      ...TaskStatus.values.map((status) => ChoiceChip(
                            label: Text(status.name),
                            selected: _selectedStatus == status,
                            onSelected: (selected) {
                              setState(() => _selectedStatus = status);
                            },
                          )),
                    ],
                  ),
                  const SizedBox(height: 24),
                  Row(
                    children: [
                      Expanded(
                        child: OutlinedButton(
                          onPressed: () {
                            setState(() {
                              _selectedTaskType = null;
                              _selectedStatus = null;
                            });
                          },
                          child: const Text('Reset'),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: ElevatedButton(
                          onPressed: () {
                            Navigator.pop(context);
                            _loadTasks();
                          },
                          child: const Text('Apply'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
} 