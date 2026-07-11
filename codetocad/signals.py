"""Streaming signal filters for sensor data.

Each filter is a callable object (``filtered = filter(sample)``), so it can
be applied sample-by-sample in a control loop or mapped over an
``EventStream``::

    smooth = communication.telemetry.map(lambda m: m["value"]).map(
        LowPassFilter(alpha=0.2)
    )

``apply_filter`` runs a filter over a whole numpy array at once.
"""

from __future__ import annotations

from collections import deque

import numpy as np


class LowPassFilter:
    """First-order exponential low-pass: ``y += alpha * (x - y)``.

    ``alpha`` in (0, 1]; smaller is smoother. For a cutoff frequency ``fc``
    sampled at ``fs``, use ``alpha = dt / (dt + 1/(2*pi*fc))`` with
    ``dt = 1/fs``."""

    def __init__(self, alpha: float):
        if not 0 < alpha <= 1:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = float(alpha)
        self.value: float | None = None

    def __call__(self, sample: float) -> float:
        if self.value is None:
            self.value = float(sample)
        else:
            self.value += self.alpha * (float(sample) - self.value)
        return self.value

    def reset(self):
        self.value = None


class MovingAverageFilter:
    """Simple moving average over the last ``window`` samples."""

    def __init__(self, window: int):
        if window < 1:
            raise ValueError("window must be >= 1")
        self._samples: deque[float] = deque(maxlen=window)

    def __call__(self, sample: float) -> float:
        self._samples.append(float(sample))
        return float(np.mean(self._samples))

    def reset(self):
        self._samples.clear()


class MedianFilter:
    """Median of the last ``window`` samples; robust to encoder/ADC spikes."""

    def __init__(self, window: int):
        if window < 1:
            raise ValueError("window must be >= 1")
        self._samples: deque[float] = deque(maxlen=window)

    def __call__(self, sample: float) -> float:
        self._samples.append(float(sample))
        return float(np.median(self._samples))

    def reset(self):
        self._samples.clear()


def apply_filter(filter_instance, samples) -> np.ndarray:
    """Run a streaming filter over an array of samples."""
    return np.array([filter_instance(sample) for sample in np.asarray(samples)])
