boolean arrastandoP = false;
boolean arrastandoQ = false;

float plx = 100;
float p2x = 300;
float p3x = 400;
float p4x = 500;

float ply = 400;
float p2y = 150;
float p3y = 400;
float p4y = 150;


void setup() {
  size(550, 500);
}

void draw() {
  background(196,196,196);
  noFill();
  if(arrastandoP)
  {
    p2x = mouseX;
    p2y = mouseY;
  }
  else if(arrastandoQ)
  {
    p3x = mouseX;
    p3y = mouseY;
  }
  beginShape();
  for(float i = 0; i <= 1; i += 0.01) {
    float ax = plx + i*(p2x-plx);
    float ay = ply + i*(p2y-ply);
    float bx = p2x + i*(p3x-p2x);
    float by = p2y + i*(p3y-p2y);
    float cx = p3x + i*(p4x-p3x);
    float cy = p3y + i*(p4y-p3y);
    float dx = ax + i*(bx-ax);
    float dy = ay + i*(by-ay);
    float ex = bx + i*(cx-bx);
    float ey = by + i*(cy-by);
    float fx = dx + i*(ex-dx);
    float fy = dy + i*(ey-dy);
    vertex(fx, fy);
  }
  endShape();
  fill(255, 0, 0);
  circle(plx, ply, 5);
  circle(p2x, p2y, 5);
  circle(p3x, p3y, 5);
  circle(p4x, p4y, 5);
}

void mousePressed()
{
    if(dist(p2x,p2y,mouseX,mouseY)<10)
    {
      arrastandoP = true;
    }
    if(dist(p3x,p3y,mouseX,mouseY)<10)
    {
      arrastandoQ = true;
    }
  
}

void mouseReleased()
{
  arrastandoP = false;
  arrastandoQ = false;
}
