# pylogz
 Super basic logger used in personal projects.

---

Why should you use this? You probably shouldn't.

---

## Quickstart

```bash
pip install --upgrade pylogz
```

## Usage

```python
from logz import get_logger 

logger = get_logger(name='libname', log_level='info', *args, **kwargs)
logger.info('...')

### Multi lib usage, threadsafe-ish

from logz import get_cls_logger
get_logger = get_cls_logger(name='libname_1', log_level='info', *args, **kwargs)
get_logger2 = get_cls_logger(name='libname_2', log_level='info', *args, **kwargs)

# Now you can call the get_logger function from any submodule.
logger = get_logger()
logger.info('hi')
"""
2021-12-03 03:36:26Z [libname_1] <stdin>.<module>             hi
"""

logger2 = get_logger2()
logger2.info('hi')
"""
2021-12-03 03:36:26Z [libname_2] <stdin>.<module>             hi
"""
```