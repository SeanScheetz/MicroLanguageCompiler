#include <stdio.h>

// Testing that you can pass-by-reference in a recursion call.
void fib(int x, int* y) {
  if (x <= 1) {
    *y = x;
  }
  else {
    int a, b;
    fib(x-1, &a);
    fib(x-2, &b);
    *y = a + b;
  }
}

int main() {
  int f = 8;
  int x;
  fib(f, &x);
  printf("%d\n", x);
  return 0;
}
