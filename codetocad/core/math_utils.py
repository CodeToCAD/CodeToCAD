def linspace(start: float, stop: float, steps: int, endpoint=True):
    # References https://gist.github.com/pmav99/d124872c879f3e9fa51e
    if endpoint:
        step = (stop - start) / (steps - 1)
    else:
        step = (stop - start) / steps

    for i in range(steps):
        yield start + step * i
