// Complex pass by reference

int foo(int* x, int* y) {
  x = x + 1;
  y = y + 1;
  return x + y;
}

int main() {
  int a = 0;
  int b = foo(a);
  printf("%d\t%d\n", a, b);

  return 0;
}
