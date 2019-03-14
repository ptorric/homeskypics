//
//
//


class APoint {
  constructor(x, y, w) {
    this.x = x;
    this.y = y;
    this.weight = w;
  }
}

class ImgData {
  construction(theName, theImage) {
    this.name = theName;
    this.image = theImage;
    this.cm = new APoint(0, 0);
    this.height = this.image.shape;
    this.width = this.image.shape
  }

  setPoints(newPoints) {
    this.points = newPoints;
  }

  centerOfMass() {
    return this.cm;
  }

  calculateCenterOfMass() {
    if (this.points.length == 0) {
      return this.cm = new APoint(0, 0);
    }
    var sumX = 0;
    var sumY = 0;
    var index = this.points.length;
    this.points.forEach(function(point) {
      sumX += point.x * point.weight;
      sumY += point.y * point.weight;
    });
    return this.cm = new APoint(sumX / index, sumY / index);
  }

  calculateMeanDistance(reference) {
      if (this.points.length == 0)
        return 0;

      var cumulative = 0
      var index = this.points.length;
      var deltaX = 0;
      var deltaY = 0;

      this.points.forEach(function(point) {
          deltaX += point.x - reference.x
          deltaY += point.y - reference.y
          cumulative += Math.sqrt(deltaX*deltaX+deltaY*deltaY)
      });

      return cumulative/index;
    }
}
