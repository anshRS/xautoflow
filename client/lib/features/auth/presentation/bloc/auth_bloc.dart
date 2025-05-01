import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:client/common/entities/user.dart';
import 'package:client/features/auth/domain/usecases/user_login_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_signup_usecase.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

part 'auth_event.dart';
part 'auth_state.dart';

class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final UserSignUpUseCase _userSignUpUseCase;
  final UserLoginUseCase _userLoginUseCase;
  final AppUserCubit _appUserCubit;

  AuthBloc({
    required UserSignUpUseCase userSignUpUseCase,
    required UserLoginUseCase userLoginUseCase,
    required AppUserCubit appUserCubit,
  }) : _userSignUpUseCase = userSignUpUseCase,
       _userLoginUseCase = userLoginUseCase,
       _appUserCubit = appUserCubit,
       super(AuthInitial()) {
    on<AuthEvent>((_, emit) => emit(AuthLoadingState()));
    on<AuthSignUpEvent>(_onAuthSignUpEvent);
    on<AuthLoginEvent>(_onAuthLoginEvent);
  }

  // SignUp user event handler
  void _onAuthSignUpEvent(AuthSignUpEvent event, Emitter<AuthState> emit) async {
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
    final res = await _userLoginUseCase(
      UserLoginParams(email: event.email, password: event.password),
    );

    res.fold(
      (l) => emit(AuthFailureState(l.message)),
      (r) => _emitAuthSuccess(r, emit),
    );
  }

  void _emitAuthSuccess(User user, Emitter<AuthState> emit) {
    _appUserCubit.updateUser(user);
    emit(AuthLoginSuccessState(user));
  }
}
