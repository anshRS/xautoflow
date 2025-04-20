import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:logger/logger.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  final Dio _dio = Dio();
  final Logger _logger = Logger();
  
  ApiService() {
    _dio.options.baseUrl = baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 5);
    _dio.options.receiveTimeout = const Duration(seconds: 10);
    
    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        // Get API key from shared preferences
        final prefs = await SharedPreferences.getInstance();
        final apiKey = prefs.getString('api_key');
        
        if (apiKey != null) {
          options.headers['X-API-Key'] = apiKey;
        }
        
        _logger.i('REQUEST[${options.method}] => PATH: ${options.path}');
        return handler.next(options);
      },
      onResponse: (response, handler) {
        _logger.i('RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
        return handler.next(response);
      },
      onError: (DioException e, handler) {
        _logger.e('ERROR[${e.response?.statusCode}] => PATH: ${e.requestOptions.path}');
        return handler.next(e);
      },
    ));
  }
  
  // Tasks API
  Future<Map<String, dynamic>> createTask(Map<String, dynamic> taskData) async {
    try {
      final response = await _dio.post('/tasks', data: taskData);
      return response.data;
    } catch (e) {
      _logger.e('Error creating task: $e');
      rethrow;
    }
  }
  
  Future<Map<String, dynamic>> getTask(String taskId) async {
    try {
      final response = await _dio.get('/tasks/$taskId');
      return response.data;
    } catch (e) {
      _logger.e('Error getting task: $e');
      rethrow;
    }
  }
  
  Future<List<dynamic>> listTasks({
    List<String>? taskTypes,
    List<String>? statuses,
    DateTime? startDate,
    DateTime? endDate,
    int skip = 0,
    int limit = 100,
  }) async {
    try {
      final queryParameters = {
        if (taskTypes != null && taskTypes.isNotEmpty) 'task_types': taskTypes,
        if (statuses != null && statuses.isNotEmpty) 'statuses': statuses,
        if (startDate != null) 'start_date': startDate.toIso8601String(),
        if (endDate != null) 'end_date': endDate.toIso8601String(),
        'skip': skip,
        'limit': limit,
      };
      
      final response = await _dio.get('/tasks', queryParameters: queryParameters);
      return response.data;
    } catch (e) {
      _logger.e('Error listing tasks: $e');
      rethrow;
    }
  }
  
  Future<Map<String, dynamic>> approveTaskPlan(String taskId, bool approved, {Map<String, dynamic>? modifiedPlan}) async {
    try {
      final data = {
        'approved': approved,
        if (modifiedPlan != null) 'modified_plan': modifiedPlan,
      };
      
      final response = await _dio.put('/tasks/$taskId/approve', data: data);
      return response.data;
    } catch (e) {
      _logger.e('Error approving task plan: $e');
      rethrow;
    }
  }
  
  // Health check
  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      _logger.e('Health check failed: $e');
      return false;
    }
  }
  
  // Save API key
  Future<void> saveApiKey(String apiKey) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('api_key', apiKey);
  }
  
  // Get API key
  Future<String?> getApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('api_key');
  }
} 