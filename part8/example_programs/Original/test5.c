// Test the ability to pass-by-value.
#include <stdio.h>

void foo1(int x) {
  printf("foo1: %d\n", x);
  x = 2*x;
  printf("foo1: %d\n", x);
}

void foo2(int x, int y) {
  printf("foo2: %d\t%d\t%d\n", x, y, x+y);
}

void foo3(char* s) {
  printf("foo3: %s\n", s);
}



int main() {
  foo1(100);

  int a = 10;
  foo1(a);
  printf("main: %d\n", a);

  int x = 10;
  foo1(x);
  printf("main: %d\n", x);

  foo2(a,x);
  printf("main: %d\t%d\n", a, x);

  char* s = "A Lannister always pays his debts.";
  foo3(s);
  printf("main: %s\n", s);

  return 0;
}
