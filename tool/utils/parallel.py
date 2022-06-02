# This module was developed by Andrzej Zielezinski from Department of Computational Biology at Adam Mickiewicz University in Poznan
from typing import Dict, Collection, Callable

import joblib
from tqdm.auto import tqdm


class Parallel(joblib.Parallel):
    """
    The modification of joblib.Parallel
    with a TQDM progress bar
    according to Nth (modified)
    (https://stackoverflow.com/questions/37804279/how-can-we-use-tqdm-in-a-parallel-execution-with-joblib)
    """

    def __init__(self,
                 parallelized_function: Callable,
                 input_collection: Collection,
                 kwargs: Dict = None,
                 n_jobs=None,
                 backend=None,
                 verbose=0,
                 timeout=None,
                 pre_dispatch='2 * n_jobs',
                 batch_size='auto',
                 temp_folder=None, max_nbytes='1M', mmap_mode='r',
                 prefer=None,
                 require=None):

        joblib.Parallel.__init__(self, n_jobs, backend, verbose, timeout,
                                 pre_dispatch, batch_size, temp_folder,
                                 max_nbytes, mmap_mode, prefer, require)
        kwargs = {} if not kwargs else kwargs
        with tqdm(total=len(input_collection)) as self._progress:
            self.result = self.__call__((joblib.delayed(parallelized_function)(e, **kwargs)) for e in input_collection)

    def print_progress(self):
        self._progress.n = self.n_completed_tasks
        self._progress.refresh()
