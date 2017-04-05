
__all__ = ['openUSPTO', 'usptoData']
__docformat__ = 'restructuredtext'

# Let users know if they're missing any of our hard dependencies
hard_dependencies = ("xml","zipfile","gzip","bz2")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(dependency)

if missing_dependencies:
    raise ImportError("Missing required dependencies {0}".format(missing_dependencies))
del hard_dependencies, dependency, missing_dependencies

from uspto.util import (openUSPTO,usptoData,getMadridEvents,
                        getMadridFiling,getForeignApplications,
                        getPriorApplications,getDesignSearch,getFileOwners,
                        getCorrespondent,getClassificationCodes,
                        getClassifications,getFileStatements,getFileEvent,
                        getFileHeader,getDetails)
