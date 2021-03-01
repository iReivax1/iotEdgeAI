import 'package:async/async.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart';
import 'package:iotClient/Connection/network.dart';
import 'package:permission_handler/permission_handler.dart';

class Upload extends StatefulWidget {
  @override
  _UploadState createState() => _UploadState();
}

class _UploadState extends State<Upload> {
  File _image;
  final picker = ImagePicker();

  Future getImage() async {
    final pickedFile = await picker.getImage(source: ImageSource.camera);
    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
      } else {
        print('No image selected.');
      }
    });
  }

  Future getImageFromGallery() async {
    final pickedFile = await picker.getImage(source: ImageSource.gallery);
    setState(() {
      if (pickedFile != null) {
        _image = File(pickedFile.path);
      } else {
        print('No image selected.');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
      appBar: AppBar(
        title: Text("Upload Image"),
      ),
      body: SingleChildScrollView(
        child: Container(
            child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              _image == null
                  ? new Text("No image selected")
                  : new Container(
                      child: Image.file(
                        _image,
                      ),
                    ),
              Container(
                  child: RaisedButton(
                      color: Colors.blue,
                      textColor: Colors.white,
                      child: Text(
                        "Take a photo",
                      ),
                      onPressed: () async {
                        if (!await Permission.camera.isGranted) {
                          await Permission.camera.request();
                          getImage();
                        } else {
                          getImage();
                        }
                      })),
              Container(
                child: RaisedButton(
                    color: Colors.blue,
                    textColor: Colors.white,
                    child: Text(
                      "Choose photo from phone",
                    ),
                    onPressed: () async {
                      if (!await Permission.photos.isGranted) {
                        await Permission.photos.request();
                        openAppSettings();
                      } else {
                        getImageFromGallery();
                      }
                    }),
              ),
              SizedBox(height: 20),
              RaisedButton(
                color: Colors.blue,
                textColor: Colors.white,
                child: Text("Upload to server"),
                onPressed: () {
                  uploadImageToServer(_image);
                },
              ),
              SizedBox(height: 20),
            ],
          ),
        )),
      ),
    );
  }

  uploadImageToServer(File imageFile) async {
    print("attempting to connecto server......");
    var stream =
        new http.ByteStream(DelegatingStream.typed(imageFile.openRead()));
    var length = await imageFile.length();
    print(length);

    var uri = Uri.parse('http://20.198.224.77/predict');
    print("connection established.");
    var request = new http.MultipartRequest("POST", uri);
    var multipartFile = new http.MultipartFile('file', stream, length,
        filename: basename(imageFile.path));
    //contentType: new MediaType('image', 'png'));

    request.files.add(multipartFile);
    var response = await request.send();
    print(response.statusCode);
  }
}
