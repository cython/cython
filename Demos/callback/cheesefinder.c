/*
 *   An example of a C API that provides a callback mechanism.
 */

#include "cheesefinder.h"

static char *cheeses[] = {
  "cheddar",
  "camembert",
  "that runny one",
  0
};

void find_cheeses(cheesefunc user_func, void *user_data) {
  char **p = cheeses;
  while (*p) {
    user_func(*p, user_data);
    ++p;
  }
}

