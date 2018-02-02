class AppError(Exception): pass

class DBNotLoaded(AppError):
    msm = "The db was not loaded"

