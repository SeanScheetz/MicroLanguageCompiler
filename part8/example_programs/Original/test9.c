// Implementing a sin function.
// (Note: Algorithmically, this is a terrible way to generate e.  Don't change it.)
#include <stdio.h>

// Compute x!.   You may change this to return a float if needed.
int fact(int x) {   // Testing recursion.  No credit for submission rewritten in closed form.
  if (x <= 1) {
    return 1;
  }

  return x*fact(x-1);
}

// Compute the value of the numerical constant e. 
float e() {
  int i;
  float s = 0;
  for (i = 0; i <= 10; i++) {   // Its assumed you will be substituing a "while" loop
    s = s + 1.0/fact(i);        // in your own code.  (You are not expected to add
  }                             // a for loop to the language.)
  return s;
} 


int main() {
  int x;
  scanf("%d", &x);
  printf("%d\n", fact(x));  // This will only be tested in small values of x -- you
                            // are not expcted to deal with potential overflow.
  printf("%f\n", e());
  return 0;
}
