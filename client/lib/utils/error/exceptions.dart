abstract class AppException implements Exception {
  final String message;
  const AppException(this.message);

  @override
  String toString() => message;
}

class AuthException extends AppException {
  const AuthException(super.message);
}

class ServerException extends AppException {
  const ServerException(super.message);
}

class ValidationException extends AppException {
  const ValidationException(super.message);
}

class NotFoundException extends AppException {
  const NotFoundException(super.message);
}

class InternalServerException extends AppException {
  const InternalServerException(super.message);
}