import cProfile
import pstats
import io
from pstats import SortKey
import pytest

pr = cProfile.Profile()
pr.enable()
for _ in range(5):
    pytest.main()
pr.disable()
s = io.StringIO()
sortby = SortKey.CUMULATIVE
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
with open('profile_results.csv', 'w') as f:
    ps.dump_stats('profile_results.pstat')
    ps = pstats.Stats('profile_results.pstat')
    ps.sort_stats(SortKey.TIME).print_stats()
    ps.sort_stats(SortKey.CUMULATIVE).print_stats()
    ps.sort_stats(SortKey.FILENAME).print_stats()
print(s.getvalue())
