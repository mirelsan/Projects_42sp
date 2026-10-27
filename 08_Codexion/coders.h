/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coders.h                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/27 00:24:24 by username          #+#    #+#             */
/*   Updated: 2026/10/27 01:27:26 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODERS_H
# define CODERS_H

# include <stdio.h> // printf
# include <stdlib.h> // malloc free
# include <unistd.h> // write, usleep
# include <stdbool.h>
# include <pthread.h> // mutex: init destrou lock unlock
// threads: create join detach
# include <sys/time.h> //gettimeofday
# include <limits.h> // INT_MAX
# include <string.h> // FOR strcmp
# include <errno.h>
// Reset code
# define RST "\033[0m"

// Bold Foreground Colors
# define BOLD_BLACK "\033[1;30m"
# define BOLD_RED "\033[1;31m"
# define BOLD_GREEN "\033[1;32m"
# define BOLD_YELLOW "\033[1;33m"
# define BOLD_BLUE "\033[1;34m"
# define BOLD_MAGENTA "\033[1;35m"
# define BOLD_CYAN "\033[1;36m"
# define BOLD_WHITE "\033[1;37m"

// define scheduler types

# define SCHEDULER_FIFO 0
# define SCHEDULER_EDF 1
# define SCHEDULER_LIFO 2

// *** structures ***

//code more readable
typedef pthread_mutex_t		t_mtx;
//IOU for compiler
typedef struct s_workspace	t_workspace;
typedef struct s_coder		t_coder;
typedef struct s_dongle		t_dongle;

// SCHEDULER FIFO AND EDF

typedef struct s_request
{
	t_coder	*coder;
	long	key;
	long	seq;
}	t_request;

// HEAP
typedef struct s_heap
{
	t_request	*items;
	int			size;
}	t_heap;

// DONGLE
typedef struct s_dongle
{
	t_mtx			dongle;
	int				dongle_id;
	bool			in_use;
	long			available_at;
	pthread_cond_t	cond;
	t_heap			queue;
	long			next_seq;
}	t_dongle;

// CODER

typedef struct s_coder
{
	int			id;
	long		number_compiles;
	bool		bournout;
	long		last_compile_time;
	// time passed from last compile
	t_mtx		progress_mutex;
	t_dongle	*first_dongle;
	t_dongle	*second_dongle;
	// coder is a thread
	pthread_t	thread_id;
	t_workspace	*workspace;
}	t_coder;

// WORKSPACE

typedef struct s_workspace
{
	long		number_of_coders;
	long		time_to_burnout;
	long		time_to_compile;
	long		time_to_debug;
	long		time_to_refactor;
	long		number_of_compiles_required;
	// [5] | FLAG if -1
	long		dongle_cooldown;
	long		scheduler;
	// SCHED_FIFO (0) or SCHED_EDF (1)
	long		start_simulation;
	//
	bool		end_simulation;
	// a coder boutnout
	t_mtx		log_mutex;
	// Protection for the logs (printf/write)
	t_dongle	*dongles;
	// attay dongles
	t_coder		*coders;
	// array
	t_mtx		end_mutex;
}	t_workspace;

// OPCODE for mutex | thread functions

typedef enum e_opcode
{
	LOCK,
	UNLOCK,
	INIT,
	DESTROY,
	CREATE,
	JOIN,
}	t_opcode;

// Container of the data
// ./coder 5 800 200 200 [5]

// parsing
void		parse_input(t_workspace *workspace, char **av);
long		ft_atoi(const char *str);

// utils
void		error_exit(const char *error);

// safe functions
void		*safe_malloc(size_t bytes);
void		safe_thread_handle(pthread_t *thread, void *(*foo)(void *),
				void *data, t_opcode opcode);
void		safe_mutex_handle(t_mtx *mutex, t_opcode opcode);
void		data_init(t_workspace *workspace);

// time functions
long		get_time_ms(void);
long		get_elapsed_time(long start_simulation);
void		safe_cond_handle(pthread_cond_t *cond, t_opcode opcode);

// LOGGER

typedef enum e_log_event
{
	TAKE_DONGLE,
	COMPILING,
	DEBUGGING,
	REFACTORING,
	BURNOUT,
}	t_log_event;

void		*coder_routine(void *arg);
void		log_event(t_coder *coder, t_log_event event);
void		cleanup_data(t_workspace *ws);

// DONGLE FUNCTIONS

void		release_dongle(t_dongle *dongle, long cooldown);
bool		take_dongle(t_coder *coder, t_dongle *dongle);
void		wait_for_turn(t_coder *coder, t_dongle *dongle, t_workspace *ws);
// MONITOR FUNCTIONS

void		*monitor_routine(void *arg);
bool		compile_target_reached(t_coder *coder);
bool		simulation_over(t_workspace *ws);
void		stop_simulation(t_workspace *ws);

void		heap_push(t_heap *heap, t_request request);
t_request	heap_pop(t_heap *heap);
t_request	heap_peek(t_heap *heap);

#endif
