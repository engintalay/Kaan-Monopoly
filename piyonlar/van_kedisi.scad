union() {
    sphere(r=8);
    translate([0,0,8]) sphere(r=5);
    translate([-3,3,13]) cone();
    translate([3,3,13]) cone();
}

module cone() {
    cylinder(h=4, r1=1.5, r2=0);
}
