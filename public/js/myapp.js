//
// registers:
// r1 full, r2 ed r3 scaled = visuals
//
// load file r1
// load file r2
// addr1 r2
// copyr1 r3
//
var myApp = new Vue({
  el: '#myApp',
  data: {
    w: 1024,
    h: 768,
    x: 0,
    y: 0,
    ax: 0,
    ay: 0,
    xw: 0,
    yw: 0,
    soglia: 0,
    element: undefined,
    click: false,
    imgData: {},
    scene: {},
    camera: {},
    renderer: {},
    controls: {},
    cv: false,
    msg: '',
  },
  methods: {

    click1: function(event) {
      this.click = true;
      this.x = event.offsetX;
      this.y = event.offsetY;
      console.log('x=' + this.x + ' y=' + this.y);
    },
    click2: function(event) {
      this.click = false;
      this.xw = event.offsetX - this.x;
      this.yw = event.offsetY - this.y;

      /*
      this.x=0;
      this.y=0;
      this.xw=this.imgData.width;
      this.yw=this.imgData.height;
      */
      console.log('xw=' + this.xw + ' yw=' + this.yw);
      //this.draw();
      //this.add2();
      this.vis();
    },
    move: function(event) {
      if (this.click) {
        //        console.log(event);
      }
      this.ax = event.offsetX;
      this.ay = event.offsetY;
    },
    vis: function() {
      var data = new vis.DataSet();

      var thecanvas = this.$refs['immagine'];
      var ctx = thecanvas.getContext("2d");
      var imgData = ctx.getImageData(0, 0, thecanvas.width, thecanvas.height);

      console.log('x=' + this.x + ' y=' + this.y + ' xw=' + this.xw + ' yw=' + this.yw);

      var step = 1;
      for (var x = 0; x < this.xw; x += step) {
        for (var y = 0; y < this.yw; y += step) {
          var pos = (this.y + y) * imgData.width * 4 + (this.x + x) * 4;
          var r = imgData.data[pos];
          var g = imgData.data[pos + 1];
          var b = imgData.data[pos + 2];
          var a = imgData.data[pos + 3];
          var v = r + g + b;

          console.log('x=' + x + ' y=' + y + ' v=' + v);
          data.add({
            x: x,
            y: -y,
            z: v,
            style: v,
          });
        }
      }

      // specify options
      var options = {
        width: '800px',
        height: '600px',
        style: 'surface',
        showPerspective: true,
        showGrid: true,
        showShadow: false,
        keepAspectRatio: true,
        // verticalRatio: 0.5
      };

      // create a graph3d
      var container = document.getElementById('visgraph');
      graph3d = new vis.Graph3d(container, data, options);
      graph3d.setCameraPosition({
        horizontal: 0.0,
        vertical: 0.5,
        distance: 1.7
      });
    },
    draw: function() {
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(90, window.innerWidth / window.innerHeight, 0.1, 1000);
      this.camera.position.z = 5;

      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(window.innerWidth, window.innerHeight);

      if (this.element != undefined)
        document.body.removeChild(this.element);
      this.element = document.body.appendChild(this.renderer.domElement);

      this.renderer.render(this.scene, this.camera);

      this.controls = new THREE.OrbitControls(this.camera);

      //controls.update() must be called after any manual changes to the camera's transform
      //      this.camera.position.set( 0, 20, 100 );
      this.controls.autoRotate = false;
      this.controls.update();
      var self = this;

      function animate() {
        // console.log('animate');
        requestAnimationFrame(animate);
        self.controls.update();
        self.renderer.render(self.scene, self.camera);
      }
      animate();
    },

    add2: function() {
      console.log('add2');
      var material = new THREE.LineBasicMaterial({
        color: 0x00ff00
      });
      var geometry = new THREE.Geometry();
      var x0 = 0; // -(this.w/4)
      var z0 = -50;

      var thecanvas = this.$refs['immagine'];
      var ctx = thecanvas.getContext("2d");
      var imgData = ctx.getImageData(0, 0, thecanvas.width, thecanvas.height);

      var y1 = this.y;
      var y2 = y1 + this.yw;
      var x1 = this.x;
      var x2 = x1 + this.xw;

      for (var y = y1; y < y2; y++) {
        var yd = y - y1;
        geometry.vertices.push(new THREE.Vector3(0, -yd * 0.1, 0));
        for (var i = x1; i < x2; i++) {
          var pos = y * imgData.width * 4 + i * 4;
          var r = imgData.data[pos];
          var g = imgData.data[pos + 1];
          var b = imgData.data[pos + 2];
          var a = imgData.data[pos + 3];

          //var z=(r+g+b)/3;
          var z = r;
          var xd = i - x1;
          //console.log('x='+i+' y='+y+' z='+z+' pos='+pos+' rgba='+r+g+b+a);
          geometry.vertices.push(new THREE.Vector3(xd * 0.1, -yd * 0.1, z * 0.1));
        }
        geometry.vertices.push(new THREE.Vector3((x2 - x1) * 0.1, -yd * 0.1, 0));
        geometry.vertices.push(new THREE.Vector3(0, -yd * 0.1, 0));
      }


      for (var i = x1; i < x2; i++) {
        var xd = i - x1;
        geometry.vertices.push(new THREE.Vector3(xd * 0.1, 0, 0));
        for (var y = y1; y < y2; y++) {
          var pos = y * imgData.width * 4 + i * 4;
          var r = imgData.data[pos];
          var g = imgData.data[pos + 1];
          var b = imgData.data[pos + 2];
          var a = imgData.data[pos + 3];

          //var z=(r+g+b)/3;
          var z = r;
          var yd = y - y1;
          // console.log('x='+i+' y='+y+' z='+z);
          geometry.vertices.push(new THREE.Vector3(xd * 0.1, -yd * 0.1, z * 0.1));
        }
        geometry.vertices.push(new THREE.Vector3(xd * 0.1, -(y2 - y1) * 0.1, 0));
        geometry.vertices.push(new THREE.Vector3(xd * 0.1, 0, 0));
      }


      var line = new THREE.Line(geometry, material);
      this.scene.add(line);
      this.renderer.render(this.scene, this.camera);
    },

    add: function() {
      var geometry = new THREE.BoxGeometry(1, 1, 1);
      var material = new THREE.MeshBasicMaterial({
        color: 0x00ff00
      });
      var cube = new THREE.Mesh(geometry, material);
      this.scene.add(cube);
      this.renderer.render(this.scene, this.camera);
    },

    clona: function(img) {
      var c2 = this.$refs['immagine']; // document.getElementById('immagine');
      var ctx = c2.getContext("2d");
      var copia = ctx.createImageData(img);
      copia.data.set(img.data);
      console.log(copia);

      return copia;
    },

    display: function(img) {
      var c2 = this.$refs['immagine']; // document.getElementById('immagine');
      var ctx = c2.getContext("2d");
      ctx.putImageData(img, 0, 0);
    },

    filter: function() {
      var buf = this.clona(this.imgData);

      for (var i = 0; i < buf.data.length; i += 4) {
        var v = (buf.data[i] + buf.data[i + 1] + buf.data[i + 2]) / 3;
        if (v < this.soglia) {
          buf.data[i] = 0;
          buf.data[i + 1] = 0;
          buf.data[i + 2] = 0;
        }
      };
      this.display(buf);
    },

    load: function(e) {
      console.log('load');
      var self = this;
      let imgElement = document.getElementById("imageSrc");
      imgElement.src = URL.createObjectURL(e.target.files[0]);
      this.msg="image loading...";
    },

    load2: function(e) {
      console.log('load2');
      let imgElement = document.getElementById("imageSrc");
      let mat = cv.imread(imgElement);
      cv.imshow('immagine', mat);
      mat.delete();
      this.msg="image processed";
    },
    histo: function() {
      let src = cv.imread('immagine');
      cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY, 0);
      let srcVec = new cv.MatVector();
      srcVec.push_back(src);
      let accumulate = false;
      let channels = [0];
      let histSize = [256];
      let ranges = [0, 255];
      let hist = new cv.Mat();
      let mask = new cv.Mat();
      let color = new cv.Scalar(255, 255, 255);
      let scale = 2;
      // You can try more different parameters
      cv.calcHist(srcVec, channels, mask, hist, histSize, ranges, accumulate);
      let result = cv.minMaxLoc(hist, mask);
      let max = result.maxVal;
      let dst = new cv.Mat.zeros(src.rows, histSize[0] * scale,
                                 cv.CV_8UC3);
      // draw histogram
      for (let i = 0; i < histSize[0]; i++) {
          let binVal = hist.data32F[i] * src.rows / max;
          let point1 = new cv.Point(i * scale, src.rows - 1);
          let point2 = new cv.Point((i + 1) * scale - 1, src.rows - binVal);
          cv.rectangle(dst, point1, point2, color, cv.FILLED);
      }
      cv.imshow('immaginetmp', dst);
      src.delete(); dst.delete(); srcVec.delete(); mask.delete(); hist.delete();
    },
    bw: function() {
      let src = cv.imread('immagine');
      let dst = new cv.Mat();
      // To distinguish the input and output, we graying the image.
      // You can try different conversions.
      cv.cvtColor(src, dst, cv.COLOR_RGBA2GRAY);
      cv.imshow('immagine', dst);
      src.delete();
      dst.delete();
      this.msg="image b/w";
    },
    cerchi: function() {
      let src = cv.imread('immagine');
      let dst = cv.Mat.zeros(src.rows, src.cols, cv.CV_8U);
      let circles = new cv.Mat();
      let color = new cv.Scalar(255, 0, 0);
      cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY, 0);
      // You can try more different parameters
      cv.HoughCircles(src, circles, cv.HOUGH_GRADIENT,
                      1, 45,   20, 20,   2, 20);
      // draw circles
      for (let i = 0; i < circles.cols; ++i) {
          let x = circles.data32F[i * 3];
          let y = circles.data32F[i * 3 + 1];
          let radius = circles.data32F[i * 3 + 2];
          let center = new cv.Point(x, y);
          cv.circle(dst, center, radius, color);
      }
      cv.imshow('immaginetmp', dst);
      src.delete(); dst.delete(); circles.delete();

    },
    invert: function() {
      var thecanvas = this.$refs['immagine'];
      var ctx = thecanvas.getContext("2d");
      var imgData = ctx.getImageData(0, 0, thecanvas.width, thecanvas.height);

      // invert colors
      for (var i = 0; i < imgData.data.length; i += 4) {
        imgData.data[i] = 255 - imgData.data[i];
        imgData.data[i + 1] = 255 - imgData.data[i + 1];
        imgData.data[i + 2] = 255 - imgData.data[i + 2];
        imgData.data[i + 3] = 255;
      }
      ctx.putImageData(imgData, 0, 0);
    },
    openCvReady: function() {
      this.cv = true;
    },
  },
});
