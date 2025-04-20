import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:client/core/models/task.dart';
import 'package:client/core/services/api_service.dart';

// Events
abstract class TasksEvent {}

class LoadTasks extends TasksEvent {}

class CreateTask extends TasksEvent {
  final TaskCreate task;

  CreateTask(this.task);
}

class UpdateTask extends TasksEvent {
  final Task task;

  UpdateTask(this.task);
}

class DeleteTask extends TasksEvent {
  final String taskId;

  DeleteTask(this.taskId);
}

class ExecuteTask extends TasksEvent {
  final String taskId;

  ExecuteTask(this.taskId);
}

// States
abstract class TasksState {}

class TasksInitial extends TasksState {}

class TasksLoading extends TasksState {}

class TasksLoaded extends TasksState {
  final List<Task> tasks;

  TasksLoaded(this.tasks);
}

class TasksError extends TasksState {
  final String message;

  TasksError(this.message);
}

class TaskExecuting extends TasksState {
  final String taskId;

  TaskExecuting(this.taskId);
}

class TaskExecuted extends TasksState {
  final TaskResult result;

  TaskExecuted(this.result);
}

// Bloc
class TasksBloc extends Bloc<TasksEvent, TasksState> {
  final ApiService _apiService;

  TasksBloc({ApiService? apiService}) 
      : _apiService = apiService ?? ApiService(),
        super(TasksInitial()) {
    on<LoadTasks>(_onLoadTasks);
    on<CreateTask>(_onCreateTask);
    on<UpdateTask>(_onUpdateTask);
    on<DeleteTask>(_onDeleteTask);
    on<ExecuteTask>(_onExecuteTask);
  }

  Future<void> _onLoadTasks(LoadTasks event, Emitter<TasksState> emit) async {
    emit(TasksLoading());
    try {
      final tasks = await _apiService.getTasks();
      emit(TasksLoaded(tasks));
    } catch (e) {
      emit(TasksError(e.toString()));
    }
  }

  Future<void> _onCreateTask(CreateTask event, Emitter<TasksState> emit) async {
    try {
      final newTask = await _apiService.createTask(event.task);
      if (state is TasksLoaded) {
        final currentTasks = (state as TasksLoaded).tasks;
        emit(TasksLoaded([...currentTasks, newTask]));
      }
    } catch (e) {
      emit(TasksError(e.toString()));
    }
  }

  Future<void> _onUpdateTask(UpdateTask event, Emitter<TasksState> emit) async {
    try {
      final updatedTask = await _apiService.updateTask(event.task);
      if (state is TasksLoaded) {
        final currentTasks = (state as TasksLoaded).tasks;
        final updatedTasks = currentTasks.map((task) {
          return task.id == updatedTask.id ? updatedTask : task;
        }).toList();
        emit(TasksLoaded(updatedTasks));
      }
    } catch (e) {
      emit(TasksError(e.toString()));
    }
  }

  Future<void> _onDeleteTask(DeleteTask event, Emitter<TasksState> emit) async {
    try {
      await _apiService.deleteTask(event.taskId);
      if (state is TasksLoaded) {
        final currentTasks = (state as TasksLoaded).tasks;
        final updatedTasks = currentTasks.where((task) => task.id != event.taskId).toList();
        emit(TasksLoaded(updatedTasks));
      }
    } catch (e) {
      emit(TasksError(e.toString()));
    }
  }

  Future<void> _onExecuteTask(ExecuteTask event, Emitter<TasksState> emit) async {
    try {
      emit(TaskExecuting(event.taskId));
      final result = await _apiService.executeTask(event.taskId);
      emit(TaskExecuted(result));
    } catch (e) {
      emit(TasksError(e.toString()));
    }
  }
} 