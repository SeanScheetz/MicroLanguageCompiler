// Test ability to return values.
#include <stdio.h>

#define true 0   // This will be unnecessary for you.
#define bool int // As will this.

int foo1() {
  return 10;
}

char* foo2() {  // You will, of course, use your string type instead of a char* type.
  return "Winter is coming.\n";
}

char* foo3() {
  int x;
  scanf("%d", &x);
  if (x >= 10) {
    return "Yes\n";
  }
  else {
    return "No\n";
  }
}

bool foo4() {
  return true;
}


int main() {
  printf("%d\n", foo1());
  printf("%d\n", 5*foo1() + foo1());
  printf("%s", foo2());
  printf("%s", foo3());
  if (foo4()) {
    printf("Yes\n");
  }
}
