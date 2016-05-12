def void foo():
  int i = 0;
  i = i + 1;
  write("In foo: ", i, "\n");
}

void foo2() {
  write("In foo2.\n");
}

BEGIN
  write("In main.\n");
  func foo();
  write("Returned to main.\n");
  foo();
  write("Returned to main. (Again.)\n");
  foo2();
  write("Returned to main.\n");
END
