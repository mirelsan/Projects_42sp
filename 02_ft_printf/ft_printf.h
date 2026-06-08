/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   ft_printf.h                                       :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: username <username@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/05/31 13:25:11 by username         #+#    #+#              */
/*   Updated: 2026/06/08 15:43:06 by username        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# define DECIMAL_BASE 10
# define HEX_BASE 16

# include <unistd.h>
# include <stdarg.h>
# include <string.h>
# include <stdlib.h>

int	ft_printf(const char *format, ...);

int	print_char(char c);
int	ft_print_str(const char *str);
int	print_p(void *ptr);
int	print_d(long int number);
int	print_u(unsigned int number);
int	print_x(unsigned int number, char type);
int	print_hex(unsigned long int number, char type);
int	ft_print_format(char specifier, va_list ap);

#endif
