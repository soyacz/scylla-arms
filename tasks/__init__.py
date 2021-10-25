from invoke import Collection

import tasks.sample
import tasks.sct
from libs.persisted_dicts import FilePersistedDotDict

ns = Collection(tasks.sample, tasks.sct)
ns.configure({'persisted': FilePersistedDotDict("persisted_params.json")})
