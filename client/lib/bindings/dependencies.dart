import 'package:client/bindings/auth_dependencies.dart';
import 'package:client/bindings/chat_dependencies.dart';
import 'package:client/bindings/code_dependencies.dart';
import 'package:client/bindings/profile_dependencies.dart';
import 'package:client/common/cubits/app_user/app_user_cubit.dart';
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';

final serviceLocator = GetIt.instance;

Future<void> initDependencies() async {  
  // Shared Prefs
  final sharedPrefs = await SharedPreferences.getInstance();
  serviceLocator.registerLazySingleton(() => sharedPrefs);    
  
  // Common
  serviceLocator.registerLazySingleton(() => AppUserCubit());

  initAuthDependencies();
  initProfileDependencies();
  initChatDependencies();
  initCodeDependencies();
}
