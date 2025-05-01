import 'package:client/common/widgets/custom_button.dart';
import 'package:client/common/widgets/custom_snackbar.dart';
import 'package:client/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:client/features/auth/presentation/screens/login_screen.dart';
import 'package:client/features/auth/presentation/screens/verify_screen.dart';
import 'package:client/features/auth/presentation/widgets/auth_form_field.dart';
import 'package:client/utils/validators/validation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class SignUpScreen extends StatefulWidget {
  static route() =>
      MaterialPageRoute(builder: (context) => const SignUpScreen());
  const SignUpScreen({super.key});

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final nameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    nameController.dispose();
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Flex(
            direction: Axis.vertical,
            children: [
              // Image section
              SizedBox(
                height: 460,
                child: Image.asset(
                  'assets/images/signup_image.png',
                  fit: BoxFit.cover,
                ),
              ),

              // Form Fields section
              BlocConsumer<AuthBloc, AuthState>(
                listener: (context, state) {
                  if (state is AuthFailureState) {
                    // Show Error Message
                    CustomPopUp.errorSnackBar(
                      context: context,
                      message: state.message,
                    );
                  } else if (state is AuthSignUpSuccessState) {
                    // Show Success Message
                    CustomPopUp.successSnackBar(
                      context: context,
                      message:
                          'Your account has been created! Please Check your inbox and verify your mail.',
                    );

                    // Redirect to Verify Email Screen
                    Navigator.push(
                      context,
                      VerifyEmailScreen.route(emailController.text.trim()),
                    );
                  }
                },
                builder: (context, state) {
                  return Form(
                    key: formKey,
                    child: Flex(
                      direction: Axis.vertical,
                      spacing: 24,
                      children: [
                        Column(
                          children: [
                            Text(
                              "Create Account",
                              style: theme.textTheme.headlineLarge?.copyWith(
                                color: theme.colorScheme.onSurface,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              "Create an account to explore features",
                              style: theme.textTheme.bodyLarge?.copyWith(
                                color: theme.colorScheme.onSurfaceVariant,
                              ),
                            ),
                          ],
                        ),

                        Flex(
                          direction: Axis.vertical,
                          spacing: 16,
                          children: [
                            AuthFormField(
                              label: "Name",
                              hintText: "Enter you name",
                              isHidden: false,
                              icon: Icon(Icons.account_circle),
                              controller: nameController,
                              validator:
                                  (value) => Validator.validateEmptyField(
                                    'Name',
                                    value,
                                  ),
                            ),
                            AuthFormField(
                              label: "Email",
                              hintText: "Enter you email",
                              isHidden: false,
                              icon: Icon(Icons.email_outlined),
                              controller: emailController,
                              validator:
                                  (value) => Validator.validateEmail(value),
                            ),
                            AuthFormField(
                              label: "Password",
                              hintText: "Enter you password",
                              isHidden: true,
                              icon: Icon(Icons.lock_outline),
                              controller: passwordController,
                              validator:
                                  (value) => Validator.validatePassword(value),
                            ),
                          ],
                        ),

                        Flex(
                          direction: Axis.vertical,
                          spacing: 8,
                          children: [
                            CustomButton(
                              text: "Sign Up",
                              onPressed: () {
                                if (formKey.currentState!.validate()) {
                                  context.read<AuthBloc>().add(
                                    AuthSignUpEvent(
                                      name: nameController.text.trim(),
                                      email: emailController.text.trim(),
                                      password: passwordController.text.trim(),
                                    ),
                                  );
                                }
                              },
                              loading:
                                  (state is AuthLoadingState) ? true : false,
                            ),

                            GestureDetector(
                              onTap: () {
                                Navigator.push(context, LogInScreen.route());
                              },
                              child: Text.rich(
                                TextSpan(
                                  children: [
                                    TextSpan(
                                      text: 'Already have an account? ',
                                      style: theme.textTheme.bodyLarge
                                          ?.copyWith(
                                            color:
                                                theme
                                                    .colorScheme
                                                    .onSurfaceVariant,
                                          ),
                                    ),
                                    TextSpan(
                                      text: 'Sign In',
                                      style: theme.textTheme.bodyLarge
                                          ?.copyWith(
                                            color:
                                                theme
                                                    .colorScheme
                                                    .onSurfaceVariant,
                                            fontWeight: FontWeight.bold,
                                          ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
