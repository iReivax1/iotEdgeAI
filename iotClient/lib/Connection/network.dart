import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:async';

class ImageData {
//  static String  BASE_URL ='http://192.168.1.103:5000/';
  String uri;
  String prediction;
  ImageData(this.uri, this.prediction);
}

Future<List<ImageData>> LoadImages() async {
  List<ImageData> list;
  //complete fetch ....
  var data = await http.get('20.198.224.77/api/');
  var jsondata = json.decode(data.body);
  List<ImageData> newslist = [];
  for (var data in jsondata) {
    ImageData n = ImageData(data['url'], data['prediction']);
    newslist.add(n);
  }

  return newslist;
}
