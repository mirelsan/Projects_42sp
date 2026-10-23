#include "coders.h"

//EVEN ODD dongle assigment

static void assign_dongles(t_coder *coder, t_dongle *dongle, int coder_position)
{
    int coder_nbr;

    coder_nbr = coder->workspace->number_of_coders;

    coder->first_dongle = &dongle[(coder_position + 1) % coder_nbr];
    coder->second_dongle = &dongle[(coder_position)];
// == to position
// DEADLOCK
    if (coder->id % 2)
    {
        coder->first_dongle = &dongle[coder_position];
        coder->second_dongle = &dongle[(coder_position + 1) % coder_nbr];
    }
}

static void coder_init(t_workspace *workspace)
{
    int     i;
    t_coder *coder;

    i = -1;
    while(++i < workspace->number_of_coders)
    {
        coder = workspace->coders + i;
        coder->id = i + 1;
        coder->bournout = false;
        coder->number_compiles = 0;
        coder->workspace = workspace;
        assign_dongles(coder, workspace->dongles, i);
    }
}


void data_init(t_workspace *workspace)
{
    int i;

    i = -1;
    workspace->end_simulation = false;
    safe_mutex_handle(&workspace->log_mutex, INIT);
    workspace->coders = safe_malloc(sizeof(t_coder) * workspace->number_of_coders);
    workspace->dongles = safe_malloc(sizeof(t_dongle) * workspace->number_of_coders);
    while (++i < workspace->number_of_coders)
    {
        safe_mutex_handle(&workspace->dongles[i].dongle, INIT);
        workspace->dongles[i].dongle_id = i; // super for debug
        workspace->dongles[i].in_use = false;
        workspace->dongles[i].available_at = 0;
        safe_cond_handle(dongles->cond);
    }
    coder_init(workspace);//TODO
}

