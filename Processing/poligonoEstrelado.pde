void setup(){
 size(500,500); 
}

void draw(){
  background(200);
  int margin = 20;
  float x = 0;
  float y = 0;
  float n = round(map(mouseX, 0,   width, 3, 12));
  float a = TWO_PI/n;
  float ha = a/2;
  
  float ray = (width/2) - margin;
  float ray2 = ray * map(mouseY, 0,   width, 0.3, 0.8);
  
  translate(width/2, height/2);
  beginShape();

  
  for(float i=0; i< TWO_PI;i+=a){
    float sx = x + ray2 * cos(i);
    float sy = y + ray2 * sin(i);
    vertex(sx,sy);
    
    sx = x + cos(i+ha) * ray;
    sy = y+ sin(i+ha) * ray;
    vertex(sx,sy);
  }
  endShape();
}

