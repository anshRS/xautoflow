import 'package:client/bindings/auth_dependencies.dart';
import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:get_it/get_it.dart';

final serviceLocator = GetIt.instance;

void initDependencies() {
  initAuthDependencies();
  
  // Common
  serviceLocator.registerLazySingleton(() => AppUserCubit());
}
