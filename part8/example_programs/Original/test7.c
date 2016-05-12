// Pass by reference
// You are not obligated to use this syntax.  
// Pascal uses the keyword "var": "integer foo(var x: integer)".
// C++ uses the & symbol following the parameter name.  
// Using the key word "ref" is another possibility.
#include <stdio.h>

void foo3(int* x) {
  int y;
  printf("foo3: %d\n", *x);
  scanf("%d", &y);
  *x = *x + y;
  printf("foo3: %d\n", *x);
}

void foo2(int* x) {
  int z;
  scanf("%d", &z);
  *x = *x + z;
  printf("foo2: %d\n", *x);
  foo3(x);
  printf("foo2: %d\n", *x);
}

void foo1(int* x) {
  int t;
  scanf("%d", &t);
  printf("foo1: %d\n", *x);
  *x = t*(*x);
  printf("foo1: %d\n", *x);
}

int main() {
  int x;
  scanf("%d", &x);
  printf("main: %d\n", x);
  foo1(&x);
  printf("main: %d\n", x);

  foo2(&x);
  printf("main: %d\n", x);
  return 0;
}
