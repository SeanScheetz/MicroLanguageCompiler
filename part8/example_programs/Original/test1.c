// Test whether you can handle basic function.
// Note: you are not required to have a void type.  (Acceptable
// to just return an int and ignore it.)
#include <stdio.h>

void foo() {
  int i = 0;
  i = i + 1;
  printf("In foo: %d.\n", i);
}

void foo2() {
  printf("In foo2.\n");
}

int main() {
  printf("In main.\n");
  foo();
  printf("Returned to main.\n");
  foo();
  printf("Returned to main. (Again.)\n");
  foo2();
  printf("Returned to main.\n");

  return 0;  // You are not required to provide for a return value
             // in your main function (assuming you have a main
             // function).
}
