// Test more compex functions.
#include <stdio.h>

void foo() {
  int i = 0;
  while (i < 5) {
    if (i % 2 == 0) {
      printf("%d ", i);
    }
    i = i+ 1;

  }
  printf("\n");
}

int main() {
  foo();
  printf("Done\n");
  foo();
  printf("Done\n");
  return 0;
}
