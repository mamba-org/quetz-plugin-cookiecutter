from quetz.pkgstores import PackageStore
from quetz.dao import Dao
from quetz.config import Config

def dummy_job(package_version: dict, config: Config, pkgstore: PackageStore, dao: Dao):
    # you can remove this job or change it to a different one
    # you can use the arguments in the signature to implement the job
    # if you don't need them, simply remove them
    pass

