import 'package:flutter/material.dart';

class AuthFormField extends StatelessWidget {
  final String label;
  final String hintText;
  final bool isHidden;
  final Icon icon;

  final TextEditingController controller;

  const AuthFormField({
    super.key,
    required this.label,
    required this.hintText,
    required this.isHidden,
    required this.icon,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      decoration: InputDecoration(
        prefixIcon: icon,
        labelText: label,
        hintText: hintText,
        border: const OutlineInputBorder(),
        floatingLabelBehavior: FloatingLabelBehavior.always,
      ),
      obscureText: isHidden,
      validator: (value) {
        if(value!.isEmpty) {
          return "$label is a mandatory field";
        }
        return null;
      },
    );
  }
}
