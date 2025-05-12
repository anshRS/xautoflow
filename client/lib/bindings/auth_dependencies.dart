import 'package:client/bindings/dependencies.dart';
import 'package:client/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:client/features/auth/data/datasources/auth_local_data_source_impl.dart';
import 'package:client/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:client/features/auth/data/datasources/auth_remote_data_source_impl.dart';
import 'package:client/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:client/features/auth/domain/repositories/auth_repository.dart';
import 'package:client/features/auth/domain/usecases/current_user_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_login_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_logout_usecase.dart';
import 'package:client/features/auth/domain/usecases/user_signup_usecase.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';

void initAuthDependencies() {
  // Datasource Dependency
  serviceLocator
    ..registerFactory<AuthRemoteDataSource>(() => AuthRemoteDataSourceImpl())
    ..registerFactory<AuthLocalDataSource>(
      () => AuthLocalDataSourceImpl(serviceLocator()),
    )
    
    // Repository Dependency
    ..registerFactory<AuthRepository>(
      () => AuthRepositoryImpl(serviceLocator(), serviceLocator()),
    )

    // Usecase Dependency
    ..registerFactory(() => UserSignUpUseCase(serviceLocator()))
    ..registerFactory(() => UserLoginUseCase(serviceLocator()))
    ..registerFactory(() => GetCurrentUserUsecase(serviceLocator()))
    ..registerFactory(() => UserLogoutUseCase(serviceLocator()))

    // Bloc Dependency
    ..registerLazySingleton(
      () => AuthBloc(
        userSignUpUseCase: serviceLocator(),
        userLoginUseCase: serviceLocator(),
        appUserCubit: serviceLocator(),
        currentUserUseCase: serviceLocator(),
        userLogoutUseCase: serviceLocator(),
      ),
    );
}
