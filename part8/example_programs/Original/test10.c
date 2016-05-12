#include <stdio.h>

// Test recursion by calculating fibonocci numbers.
int fib(int x) {
  if (x <= 1) {
    return x;
  }

  return fib(x-1) + fib(x-2);
}

int main() {
  int f;
  scanf("%d", &f);
  printf("%d\n", fib(f));

  return 0;
}
