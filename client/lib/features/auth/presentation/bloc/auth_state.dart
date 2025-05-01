part of 'auth_bloc.dart';

@immutable
sealed class AuthState {
  const AuthState();
}

final class AuthInitial extends AuthState {}

// Loading Auth State
final class AuthLoadingState extends AuthState {}

// Error Auth State
final class AuthFailureState extends AuthState {
  final String message;
  const AuthFailureState(this.message);
}

// Success SignUp State
final class AuthSignUpSuccessState extends AuthState {}

// Success Login State
final class AuthLoginSuccessState extends AuthState {
  final User user;
  const AuthLoginSuccessState(this.user);
}
