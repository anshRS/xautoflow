part of 'auth_bloc.dart';

@immutable
sealed class AuthEvent {}

// On SignUp Event
final class AuthSignUpEvent extends AuthEvent {
  final String name;
  final String email;
  final String password;

  AuthSignUpEvent({required this.name, required this.email, required this.password});
}

// On LogIn Event
final class AuthLoginEvent extends AuthEvent {
  final String email;
  final String password;

  AuthLoginEvent({required this.email, required this.password});  
}

// User Login Event
final class AuthIsUserLoggedIn extends AuthEvent {}

// User Logout Event
final class AuthLogoutEvent extends AuthEvent {}

// Loading Event
final class AuthStopLoadingEvent extends AuthEvent {}
