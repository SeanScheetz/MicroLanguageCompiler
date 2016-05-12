// Testing ability to call functions-from-functions.
// 474: You are only expected to call functions that were declared before the function call.
//      You do not need to enable recursion.
// 574: You need to enable direct recursion (that is, a function calling itself -- this will
//      be tested in tests 9-11), but do not need to allow for a function to call a function 
//      declared later in the program.
#include <stdio.h>

void foo1() {
  int z = 3;
  printf("foo1: %d\n", z);
}

void foo2() {
  int y = 2;
  foo1();
  printf("foo2: %d\n", y);
}

void foo3() {
  int x = 3;
  printf("foo3: %d\n", x);
}

void foo4() {
  int x = 2;
  foo3();
  printf("foo4: %d\n", x);
}

int main() {
  int x = 1;
  foo2();
  printf("main: %d\n", x);
  foo4();
  printf("main: %d\n", x);
  return 0;
}
