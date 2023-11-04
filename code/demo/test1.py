if __name__ == "__main__":
    # set to True if you want to enable tracing of the Python code
    # traces are sent to stdout. For debugging only.
    enable_trace = True
    if enable_trace:
        import trace

        tracer = trace.Trace(
            ignoredirs=[sys.prefix, sys.exec_prefix], count=0)

        # run the new command using the given tracer
        tracer.run('main()')
    else:
        main()


def main()
    return