int32_t ref_var_value = 10;
int32_t& ref_var = ref_var_value;

int32_t& ref_func(int32_t& x) { return x; }
