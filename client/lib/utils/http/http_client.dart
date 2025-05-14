import 'dart:convert';
import 'dart:io';
import 'package:client/utils/error/errors.dart';
import 'package:client/utils/error/exceptions.dart';
import 'package:http/http.dart' as http;

class HttpHelper {
  // Backend API base URL
  static const String _baseUrl = 'http://10.0.2.2:8000';

  // GET http method
  static Future<Map<String, dynamic>?> get(
    String endpoint, {
    Map<String, String>? headers,
  }) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/$endpoint'),
      headers: headers,
    );
    return _responseHandler(response);
  }

  // POST http method
  static Future<Map<String, dynamic>?> post(
    String endpoint,
    dynamic data,
  ) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/$endpoint'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );
    return _responseHandler(response);
  }

  // PUT http method
  static Future<Map<String, dynamic>?> put(
    String endpoint,
    dynamic data,
  ) async {
    final response = await http.put(
      Uri.parse('$_baseUrl/$endpoint'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );
    return _responseHandler(response);
  }

  static Future<Map<String, dynamic>?> delete(String endpoint) async {
    final response = await http.delete(Uri.parse('$_baseUrl/$endpoint'));
    return _responseHandler(response);
  }

  static Future<Map<String, dynamic>?> multipartPost(
    String endpoint, {
      required Map<String, String> fields,
      File? file,
      Map<String, String>? headers,
    }
  ) async {
    var request = http.MultipartRequest('POST', Uri.parse('$_baseUrl/$endpoint'));

    if(headers != null) {
      request.headers.addAll(headers);
    }

    request.fields.addAll(fields);

    if(file != null) {
      request.files.add(await http.MultipartFile.fromPath('avatar', file.path));
    }

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    return _responseHandler(response);
  }

  // http response handler
  static Map<String, dynamic>? _responseHandler(http.Response response) {
    switch (response.statusCode) {
      case 200: // OK
        return json.decode(response.body);

      case 201: // Created
        return json.decode(response.body);

      case 400: // Bad Request
        throw ServerException(extractError(response));

      case 401: // Unauthorized
        throw AuthException(extractError(response));

      case 403: // Forbidden
        throw AuthException(extractError(response));

      case 404: // Not Found
        throw NotFoundException(extractError(response));

      case 422: // Unprocessable Entity
        throw ValidationException(extractError(response));

      case 500: // Internal Server Error
        throw InternalServerException(extractError(response));

      default:
        throw ServerException(
          "Unhandled ${response.statusCode}: $extractError(response)",
        );
    }
  }
}
