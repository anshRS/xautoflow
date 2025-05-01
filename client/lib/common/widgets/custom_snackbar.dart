import 'package:flutter/material.dart';

class CustomPopUp {
  static customSnackBar({
    required BuildContext context,
    required String message,
    required Color backgroundColor,
    IconData? icon,
  }) {
    ScaffoldMessenger.of(context)
      ..hideCurrentSnackBar()
      ..showSnackBar(
        SnackBar(
          elevation: 0,
          behavior: SnackBarBehavior.floating,
          margin: const EdgeInsets.all(0),
          duration: const Duration(seconds: 5),
          backgroundColor: Colors.transparent,
          content: Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: backgroundColor,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: Icon(icon, color: Colors.white),
                ),
                Expanded(child: Text(message, style: const TextStyle(color: Colors.white), overflow: TextOverflow.visible,)),
              ],
            ),
          ),
        ),
      );
  }

  static successSnackBar({required BuildContext context, String message = ''}) {
    customSnackBar(
      context: context,
      message: message,
      backgroundColor: Colors.green,
      icon: Icons.check_circle,
    );
  }

  static errorSnackBar({required BuildContext context, String message = ''}) {
    customSnackBar(
      context: context,
      message: message,
      backgroundColor: Colors.redAccent,
      icon: Icons.error,
    );
  }

  static infoSnackBar({required BuildContext context, String message = ''}) {
    customSnackBar(
      context: context,
      message: message,
      backgroundColor: Colors.blueAccent,
      icon: Icons.info_outline,
    );
  }
}
