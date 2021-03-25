import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:async';

class ImageData {
  String uri;
  String prediction;
  ImageData(this.uri, this.prediction);
}

Future<List<ImageData>> LoadImages() async {
  var res = await http.get('20.198.224.77/api/');
  var res_json = json.decode(res.body);
  List<ImageData> newslist = [];
  for (var data in res_json) {
    ImageData n = ImageData(data['url'], data['prediction']);
    newslist.add(n);
  }

  return newslist;
}
