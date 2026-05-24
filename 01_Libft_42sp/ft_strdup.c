char        *ft_strdup(const char *s)
{
     char *dest;
     int i;
     int s_len;
     
     
     s_len = ft_strlen(s);
     dest = malloc(s_len + 1);
     
     if(dest == NULL)
         return (NULL);
     i = 0;
     while(i < s_len)
     {
         dest[i] = s[i];
         i++;
     }
     dest[i] = '\0';
     return(dest);
}