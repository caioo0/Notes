#ifdef lround
inline long lround(double d)
{
    return (d >= 0) ?  long(d + 0.5) : long(d - 0.5);
}
#endif
