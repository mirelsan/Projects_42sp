#include "coders.h"

// LOGGER

static const char    *event_text(t_log_event event)
{
    if (event == TAKE_DONGLE)
        return ("has taken a dongle");
    if (event == COMPILING)
        return ("is compiling");
    if (event == DEBUGGING)
        return ("is debugging");
    if (event == REFACTORING)
        return ("is refactoring");
    if (event == BURNOUT)
        return ("burned out");
    return ("unknown log event");
}

void    log_event(t_coder *coder, t_log_event event)
{
    printf("%ld %d %s\n", get_elapsed_time(coder->workspace->start_simulation), coder->id, event_text(event));
}