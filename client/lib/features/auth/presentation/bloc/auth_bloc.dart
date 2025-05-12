import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/entities/user.dart';
import 'package:client/common/usecases/usecase.dart';
import 'package:client/features/auth/domain/usecases/current_user_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_login_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_logout_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_signup_usecase.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final UserSignUpUseCase _userSignUpUseCase;
  final UserLoginUseCase _userLoginUseCase;
  final GetCurrentUserUsecase _currentUserUsecase;
  final AppUserCubit _appUserCubit;
  final UserLogoutUseCase _userLogoutUseCase;

  AuthBloc({
    required UserSignUpUseCase userSignUpUseCase,
    required UserLoginUseCase userLoginUseCase,
    required GetCurrentUserUsecase currentUserUseCase,
    required AppUserCubit appUserCubit,
    required UserLogoutUseCase userLogoutUseCase,
  }) : _userSignUpUseCase = userSignUpUseCase,
       _userLoginUseCase = userLoginUseCase,
       _currentUserUsecase = currentUserUseCase,
       _appUserCubit = appUserCubit,
       _userLogoutUseCase = userLogoutUseCase,
       super(AuthInitial()) {
    // on<AuthEvent>((_, emit) => emit(AuthLoadingState()));
    on<AuthSignUpEvent>(_onAuthSignUpEvent);
    on<AuthLoginEvent>(_onAuthLoginEvent);
    on<AuthIsUserLoggedIn>(_isUserLoggendIn);
    on<AuthLogoutEvent>(_onAuthLogoutEvent);
    on<AuthStopLoadingEvent>(_onAuthStopLoadingEvent);
  }

  void _isUserLoggendIn(
    AuthIsUserLoggedIn event,
    Emitter<AuthState> emit,
  ) async {    
    emit(AuthLoadingState());
    final res = await _currentUserUsecase(NoParams());

    res.fold(
      (l) => emit(AuthStopLoadingState()),
      (r) => _emitAuthSuccess(r, emit),
    );
  }

  // SignUp user event handler
  void _onAuthSignUpEvent(AuthSignUpEvent event, Emitter<AuthState> emit) async {
    emit(AuthLoadingState());
    final res = await _userSignUpUseCase(
      UserSignUpParams(
        name: event.name,
        email: event.email,
        password: event.password,
      ),
    );

    res.fold(
      (l) => emit(AuthFailureState(l.message)),
      (r) => emit(AuthSignUpSuccessState()),
    );
  }

  // LogIn user event handler
  void _onAuthLoginEvent(AuthLoginEvent event, Emitter<AuthState> emit) async { 
    emit(AuthLoadingState());   
    final res = await _userLoginUseCase(
      UserLoginParams(email: event.email, password: event.password),
    );

    res.fold(
      (l) => emit(AuthFailureState(l.message)),
      (r) => _emitAuthSuccess(r, emit),
    );
  }

  // Logout user event handler
  void _onAuthLogoutEvent(AuthLogoutEvent event, Emitter<AuthState> emit) async {
    final res = await _userLogoutUseCase(NoParams());

    res.fold((l) => emit(AuthFailureState(l.message)),
    (r) => _emitAuthLogout(emit),
    );
  }

  void _emitAuthSuccess(User user, Emitter<AuthState> emit) {
    _appUserCubit.updateUser(user);
    emit(AuthLoginSuccessState(user));
  }

  void _emitAuthLogout(Emitter<AuthState> emit) {
    _appUserCubit.updateUser(null);
  }

  void _onAuthStopLoadingEvent(AuthStopLoadingEvent event, Emitter<AuthState> emit) {
    emit(AuthStopLoadingState());
  }
}
