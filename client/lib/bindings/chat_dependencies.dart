import 'package:client/bindings/dependencies.dart';
import 'package:client/features/chat/data/datasources/chat_remote_datasource.dart';
import 'package:client/features/chat/data/repositories/chat_repository_impl.dart';
import 'package:client/features/chat/domain/repositories/chat_repository.dart';
import 'package:client/features/chat/domain/usecases/connect_chat_usecase.dart';
import 'package:client/features/chat/domain/usecases/disconnect_chat_usecase.dart';
import 'package:client/features/chat/domain/usecases/send_message_usecase.dart';
import 'package:client/features/chat/domain/usecases/stream_message_usecase.dart';
import 'package:client/features/chat/presentation/bloc/chat_bloc.dart';

void initChatDependencies() {
  serviceLocator
    // Datasource Dependency
    ..registerLazySingleton(() => ChatRemoteDatasource())

    // Repository Dependency
    ..registerFactory<ChatRepository>(
      () => ChatRepositoryImpl(serviceLocator()),
    )

    // Usecase Dependency
    ..registerFactory(() => SendMessageUsecase(serviceLocator()))
    ..registerFactory(() => StreamMessageUsecase(serviceLocator()))
    ..registerFactory(() => ConnectChatUsecase(serviceLocator()))
    ..registerFactory(() => DisconnectChatUsecase(serviceLocator()))
            
    // Bloc Dependency
    ..registerLazySingleton(
      () => ChatBloc(
        sendMessageUsecase: serviceLocator(),
        streamMessageUsecase: serviceLocator(),
        disconnectChatUsecase: serviceLocator(),
        connectChatUsecase: serviceLocator(),
      ),
    );
}
