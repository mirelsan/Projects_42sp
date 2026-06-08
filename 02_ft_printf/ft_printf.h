/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/31 13:25:11 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/06/07 23:51:45 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#ifndef FT_PRINTF_H
#define FT_PRINTF_H

#define DECIMAL_BASE 10
#define HEX_BASE 16

#include <unistd.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

int ft_printf(const char *format, ...);

int print_char(char c);
int ft_print_str(const char *str);
int print_p(void *ptr);
int print_d(int number);
int print_u(unsigned int number);
int print_x(unsigned int number, char type);
int print_hex(unsigned long int number, char type);
int ft_print_format(char specifier, va_list ap);

#endif