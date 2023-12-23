import numpy as np
from numpy.typing import NDArray


EPS = 1e-6


def smoothstep_np(
    low: float, high: float, val: NDArray[np.float32]
) -> NDArray[np.float32]:
    val = val.astype(np.float32)
    if low > high:
        high = -high
        low = -low
        val = -val
    res = np.zeros_like(val, dtype=np.float32)
    res[val >= high - EPS] = 1.0

    mix_bool = (val > low + EPS) & (val < high - EPS)
    mix_idxes = np.where(mix_bool)

    v_sub = val[mix_idxes]

    v_norm = (v_sub - low) / (high - low)
    v2 = v_norm * v_norm
    smoothed = 3 * v2 - 2 * v_norm * v2
    res[mix_idxes] = smoothed
    return res


def smoothstep_f(low: float, high: float, val: float) -> float:
    if low > high:
        high = -high
        low = -low
        val = -val
    if val >= high - EPS:
        return 1.0
    if val <= low + EPS:
        return 0.0

    v_norm = (val - low) / (high - low)
    v2 = v_norm * v_norm
    smoothed = 3 * v2 - 2 * v_norm * v2
    return smoothed
