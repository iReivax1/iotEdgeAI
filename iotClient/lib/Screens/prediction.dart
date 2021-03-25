class Prediction {
  final String predictedClass;
  final String score;
  final String title;
  final String timeStamp;

  Prediction({this.title, this.predictedClass, this.score, this.timeStamp});

  factory Prediction.fromJson(Map<String, dynamic> json) {
    return Prediction(
      title: json['title'],
      predictedClass: json['prediction'],
      score: json['confidence'],
      timeStamp: json['upload_time'],
    );
  }
}
