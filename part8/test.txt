def void foo():
  int i;
  i := 0;
  i := i + 1;
  write("In foo: ", i, "\n");

def void foo2():
  write("In foo2.\n");

BEGIN
  write("In main.\n");
  func foo();
  write("Returned to main.\n");
  func foo();
  write("Returned to main. (Again.)\n");
  func foo2();
  write("Returned to main.\n");
END
