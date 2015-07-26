#include "mt_cheesefinder.h"
#include <pthread.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdio.h>

//Each thread represents a mouse which steals cheese from the Python
void *steal_cheese_thr(void* user_data)
{
   long tid = (long) user_data;

   while(1) {
	   if ( cheeses_action_handler("all_cheeses", user_data) == 1 ){
	      printf("[%ld]PASS: all_cheeses found!\n", tid);
	   } else {
	      printf("[%ld] FAILED: no cheese left !\n" ,tid);
	   }

	   if (cheeses_action_handler("cheddar", user_data) == 0 ) {
	      printf("[%ld]PASS: out of cheddar!\n", tid);
	   } else {
	      printf("[%ld]FAILED: cheddar found!!\n",tid);
	   }

	   if (cheeses_action_handler("provlone", user_data) == 0 ) {
	      printf("[%ld]PASS: provlone found !!\n", tid);
	   } else {
	      printf("[%ld]FAILED: out of provlone !!\n",tid);
	   }
           sleep(1);
   }

}

//Initialize 10 mouse threads.This function is called from the Python side
void cheeses_init_pthreads(void)
{
   pthread_t thr[10];
   long i;
   for ( i = 0 ; i < 10 ; i++ )
   {
      //Create thread to periodically steal cheese from the python
      printf("C-code creating steal_cheese_thr thread[%d] !\n", i);
      pthread_create(&thr[i], NULL, steal_cheese_thr , (void*)i );
      pthread_detach(thr[i]);
    }
}

