var express = require('express');  
var app = express();  
var server = require('http').Server(app);  
const { Server } = require("socket.io");
const io = require('socket.io')(server, {
    cors: {
        origin: "http://localhost:5000",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});
app.set('port', (process.env.PORT || 5000));


app.use(express.static(__dirname + ''));
app.get('/', function(request, response) {
  response.render('index.html')
});

server.listen(app.get('port'), function() {
  console.log('Node app is running on port', app.get('port'));
});


var fs = require('fs');

path1='C:/Users/Admin/Desktop/Tesis/Actas/2019'
path2='C:/Users/Admin/Desktop/Tesis/Actas/2021'
path3='C:/Users/Admin/Desktop/Tesis/Actas/20212v'
var des2019 = fs.readdirSync(path1);
var des2021 = fs.readdirSync(path2);
var des20212v = fs.readdirSync(path3);
var temp2019=0
var temp2021=0
var temp20212v=0
var pro2019=0
var pro2021=0
var pro20212v=0
var val2019=0
var val2021=0
var val20212v=0

for (var i = 0; i<=des2019.length-1; i++){
  if("Acta"==des2019[i].split('2019')[0]){
  var t = fs.readdirSync(path1+"/"+des2019[i])
  temp2019=temp2019+t.length
}
}
for (var i = 0; i<=des2021.length-1; i++){
  if("Acta"==des2021[i].split('2021')[0]){
  var t = fs.readdirSync(path2+"/"+des2021[i])
  temp2021=temp2021+t.length
}
}
for (var i = 0; i<=des20212v.length-1; i++){
  if("Acta"==des20212v[i].split('2021')[0]){
  var t = fs.readdirSync(path3+"/"+des20212v[i])
  temp20212v=temp20212v+t.length
}
}
  

data = fs.readFileSync('2019/validas.txt',{encoding:'utf8', flag:'r'});
val2019=data.split('\n').length
data = fs.readFileSync('2021/validas.txt',{encoding:'utf8', flag:'r'});
val2021=data.split('\n').length
data = fs.readFileSync('20212v/validas.txt',{encoding:'utf8', flag:'r'});
val20212v=data.split('\n').length


var data = fs.readFileSync('2019/procesadas.txt',{encoding:'utf8', flag:'r'});
pro2019=data.split('\n').length
var data = fs.readFileSync('2021/procesadas.txt',{encoding:'utf8', flag:'r'});
pro2021=data.split('\n').length
var data = fs.readFileSync('20212v/procesadas.txt',{encoding:'utf8', flag:'r'});
pro20212v=data.split('\n').length


var a =[
          ['2019','2021','20212v'],
         [temp2019,temp2021,temp20212v],
         [pro2019,pro2021,pro20212v],
         [val2019,val2021,val20212v]
        ]


var files2021 = fs.readdirSync('2021/erroresInfo');
var files2019 = fs.readdirSync('2019/erroresInfo');
var files20212v = fs.readdirSync('20212v/erroresInfo');

var p11=(((pro2019*100)/(temp2019)).toFixed(2))+" %"
var p21=(((pro2021*100)/(temp2021)).toFixed(2))+" %"
var p31=(((pro20212v*100)/(temp20212v)).toFixed(2))+" %"

var p1=(100-((files2019.length*100)/(pro2019*16)).toFixed(2))+" %"
var p2=(100-((files2021.length*100)/(pro2021*19)).toFixed(2))+" %"
var p3=(100-((files20212v.length*100)/(pro20212v*5)).toFixed(2))+" %"

var b =[
          ['2019','2021','20212v'],
         [val2019*16,val2021*19,val20212v*5],
         [files2019.length,files2021.length,files20212v.length]
        ]

io.on('connection', (socket) => {
  socket.on('pedir2021', (msg) => {
    io.emit('estado2021', files2021);
    console.log('enviado2021')
  });
  socket.on('pedir20212v', (msg) => {
    io.emit('estado20212v', files20212v);
    console.log('enviado20212v')
  });
  socket.on('pedir2019', (msg) => {
    io.emit('estado2019', files2019);
    console.log('enviado2019')
  });
  socket.on('leerarchivo', (ruta,archivo) => {
    fs.readFile(ruta+"/erroresInfo/"+archivo+".txt", 'utf8', (err, data) => {
  io.emit('recArchivo', data);
});
    
    
  });
   socket.on('pedirtabla', (e) => {
   
  io.emit('enviartabla', a);

  });
  socket.on('pedirtabla2', (e) => {
   
  io.emit('enviartabla2', b);

  });
   socket.on('pedirporcentaje', (e) => {
   
  io.emit('enviarporcentaje', "Valido: "+p1+"    "+p2+"    "+p3);

  });
  socket.on('pedirporcentaje1', (e) => {
   
  io.emit('enviarporcentaje1', p11+"     "+p21+"     "+p31);

  });
    socket.on('pedirtotal', (e) => {
   
  io.emit('enviartotal', [temp2019,temp2021,temp20212v]);
  });
});
