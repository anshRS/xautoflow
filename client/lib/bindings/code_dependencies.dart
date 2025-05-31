import 'package:client/bindings/dependencies.dart';
import 'package:client/features/code/data/datasources/code_remote_datasource.dart';
import 'package:client/features/code/data/repositories/code_repository_impl.dart';
import 'package:client/features/code/domain/repositories/code_repository.dart';
import 'package:client/features/code/domain/usecases/connect_code_usecase.dart';
import 'package:client/features/code/domain/usecases/disconnect_code_usecase.dart';
import 'package:client/features/code/domain/usecases/send_message_usecase.dart';
import 'package:client/features/code/domain/usecases/stream_message_usecase.dart';
import 'package:client/features/code/presentation/bloc/code_bloc.dart';

void initCodeDependencies() {
  serviceLocator
    // Datasource Dependency
    ..registerLazySingleton(() => CodeRemoteDatasource())

    // Repository Dependency
    ..registerFactory<CodeRepository>(
      () => CodeRepositoryImpl(serviceLocator()),
    )

    // Usecase Dependency
    ..registerFactory(() => SendMessageUsecase(serviceLocator()))
    ..registerFactory(() => StreamMessageUsecase(serviceLocator()))
    ..registerFactory(() => ConnectCodeUsecase(serviceLocator()))
    ..registerFactory(() => DisconnectCodeUsecase(serviceLocator()))
            
    // Bloc Dependency
    ..registerLazySingleton(
      () => CodeBloc(
        sendMessageUsecase: serviceLocator(),
        streamMessageUsecase: serviceLocator(),
        disconnectCodeUsecase: serviceLocator(),
        connectCodeUsecase: serviceLocator(),
      ),
    );
}
