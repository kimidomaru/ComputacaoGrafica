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

  
void star(float x, float y, 
  float radius1, float radius2, 
  int npoints) { 
 
  float angle = TWO_PI / npoints; 
  float halfAngle = angle/2.0; 
 
  beginShape(); 
  for (float a = 0; a < TWO_PI; a += angle) { 
    float sx = x + cos(a) * radius2; 
    float sy = y + sin(a) * radius2; 
    vertex(sx, sy); 
    sx = x + cos(a+halfAngle) * radius1; 
    sy = y + sin(a+halfAngle) * radius1; 
    vertex(sx, sy);
  } 
  endShape(CLOSE);
}
