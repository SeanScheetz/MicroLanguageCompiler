// Complex pass by reference
#include <stdio.h>

int foo1(int* x, int* y) {
  *x = *x + 1;
  printf("foo1: %d %d\n", *x, *y);
  *y = *y + 1;
  printf("foo1: %d %d\n", *x, *y);
  return *x + *y;
}

void foo2(int* x) {
  int b;
  scanf("%d", &b);
  int a = *x;
  a = a + b;
  printf("foo2: %d %d\n", *x, a);
}

int main() {
  int a;
  scanf("%d", &a);
  int b = foo1(&a, &a);
  printf("main: %d %d\n", a, b);

  int c;
  scanf("%d", &c);
  foo2(&c);
  return 0;
}
