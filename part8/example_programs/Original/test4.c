// Test globals and scoping
#include <stdio.h>

int x;

void foo1() {
  printf("foo1: %d\n", x);
  x += 10;
  printf("foo1: %d\n", x);
}

void foo2() {
  printf("foo2: %d\n", x);
}

void foo3() {
  int x = 300;
  printf("foo3: %d\n", x);
}

int main() {
  x = 0;

  printf("main: %d\n", x);
  foo1();
  printf("main: %d\n", x);
  foo1();
  printf("main: %d\n", x);
  foo2();
  printf("main: %d\n", x);
  foo3();
  printf("main: %d\n", x);
  return 0;
}
