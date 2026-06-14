from statistics import mean, pvariance, pstdev


def data_range(values):
    clean_values = _clean(values)
    if not clean_values:
        return None
    return max(clean_values) - min(clean_values)


def descriptive_metrics(values):
    clean_values = _clean(values)
    if not clean_values:
        return {"mean": None, "range": None, "variance": None, "std_dev": None}

    return {
        "mean": mean(clean_values),
        "range": data_range(clean_values),
        "variance": pvariance(clean_values),
        "std_dev": pstdev(clean_values),
    }


def covariance(x_values, y_values):
    x = _clean(x_values)
    y = _clean(y_values)
    size = min(len(x), len(y))
    if size == 0:
        return None

    x = x[:size]
    y = y[:size]
    x_mean = mean(x)
    y_mean = mean(y)
    return sum((x_item - x_mean) * (y_item - y_mean) for x_item, y_item in zip(x, y)) / size


def _clean(values):
    return [float(value) for value in values if value is not None]

