import 'package:client/bindings/dependencies.dart';
import 'package:client/features/profile/data/datasources/profile_remote_data_source.dart';
import 'package:client/features/profile/data/datasources/profile_remote_data_source_impl.dart';
import 'package:client/features/profile/data/repositories/profile_repository_impl.dart';
import 'package:client/features/profile/domain/repository/profile_repository.dart';
import 'package:client/features/profile/domain/usecases/profile_update_usecase.dart';
import 'package:client/features/profile/presentation/bloc/profile_bloc.dart';

void initProfileDependencies() {
  // Datasource Dependency
  serviceLocator
    ..registerFactory<ProfileRemoteDataSource>(
      () => ProfileRemoteDataSourceImpl(),
    )

    // Repository Dependency
    ..registerFactory<ProfileRepository>(
      () => ProfileRepositoryImpl(serviceLocator()),
    )

    // Usecase Dependency
    ..registerFactory(() => ProfileUpdateUsecase(serviceLocator()))
    
    // Bloc Dependency
    ..registerLazySingleton(
      () => ProfileBloc(
        profileUpdateUsecase: serviceLocator(),
        appUserCubit: serviceLocator(),
      ),
    );
}
