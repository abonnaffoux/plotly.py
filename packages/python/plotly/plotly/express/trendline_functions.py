import pandas as pd
import numpy as np


def ols(options, x, y, x_label, y_label, non_missing):
    import statsmodels.api as sm

    add_constant = options.get("add_constant", True)
    log_x = options.get("log_x", False)
    log_y = options.get("log_y", False)

    if log_y:
        y = np.log(y)
        y_label = "log(%s)" % y_label
    if log_x:
        x = np.log(x)
        x_label = "log(%s)" % x_label
    if add_constant:
        x = sm.add_constant(x)
    fit_results = sm.OLS(y, x, missing="drop").fit()
    y_out = fit_results.predict()
    if log_y:
        y_out = np.exp(y_out)
    hover_header = "<b>OLS trendline</b><br>"
    if len(fit_results.params) == 2:
        hover_header += "%s = %g * %s + %g<br>" % (
            y_label,
            fit_results.params[1],
            x_label,
            fit_results.params[0],
        )
    elif not add_constant:
        hover_header += "%s = %g* %s<br>" % (y_label, fit_results.params[0], x_label,)
    else:
        hover_header += "%s = %g<br>" % (y_label, fit_results.params[0],)
    hover_header += "R<sup>2</sup>=%f<br><br>" % fit_results.rsquared
    return y_out, hover_header, fit_results


def lowess(options, x, y, x_label, y_label, non_missing):
    import statsmodels.api as sm

    frac = options.get("frac", 0.6666666)
    y_out = sm.nonparametric.lowess(y, x, missing="drop", frac=frac)[:, 1]
    hover_header = "<b>LOWESS trendline</b><br><br>"
    return y_out, hover_header, None


def ma(options, x, y, x_label, y_label, non_missing):
    y_out = pd.Series(y, index=x).rolling(**options).mean()[non_missing]
    hover_header = "<b>Moving Average trendline</b><br><br>"
    return y_out, hover_header, None


def ewm(options, x, y, x_label, y_label, non_missing):
    y_out = pd.Series(y, index=x).ewm(**options).mean()[non_missing]
    hover_header = "<b>EWM trendline</b><br><br>"
    return y_out, hover_header, None
