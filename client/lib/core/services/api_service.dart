import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:client/core/models/task.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';

  // Tasks
  Future<List<Task>> getTasks() async {
    final response = await http.get(Uri.parse('$baseUrl/tasks'));
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      return data.map((json) => Task.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load tasks');
    }
  }

  Future<Task> createTask(TaskCreate task) async {
    final response = await http.post(
      Uri.parse('$baseUrl/tasks'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(task.toJson()),
    );
    if (response.statusCode == 201) {
      return Task.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to create task');
    }
  }

  Future<Task> updateTask(Task task) async {
    final response = await http.put(
      Uri.parse('$baseUrl/tasks/${task.id}'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(task.toJson()),
    );
    if (response.statusCode == 200) {
      return Task.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to update task');
    }
  }

  Future<void> deleteTask(String taskId) async {
    final response = await http.delete(Uri.parse('$baseUrl/tasks/$taskId'));
    if (response.statusCode != 204) {
      throw Exception('Failed to delete task');
    }
  }

  // Task Execution
  Future<TaskResult> executeTask(String taskId) async {
    final response = await http.post(
      Uri.parse('$baseUrl/tasks/$taskId/execute'),
    );
    if (response.statusCode == 200) {
      return TaskResult.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to execute task');
    }
  }

  Future<TaskResult> getTaskResult(String taskId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/tasks/$taskId/result'),
    );
    if (response.statusCode == 200) {
      return TaskResult.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to get task result');
    }
  }
} 