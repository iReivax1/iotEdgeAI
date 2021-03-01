import 'package:flutter/material.dart';
import 'screens/upload.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'Iot',
        theme: ThemeData(
          primarySwatch: Colors.blue,
        ),
        home: Upload());
  }
}
